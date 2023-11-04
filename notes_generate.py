import textwrap
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import openai
import os
import record_audio
from pydub import AudioSegment
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import argparse


def split_audio(input_filename, output_directory, chunk_length_ms):
    # Load the audio file
    audio = AudioSegment.from_file(input_filename)
    
    # Get the total length of the audio in milliseconds
    total_length_ms = len(audio)
    
    # Split the audio into chunks and save them
    for i in range(0, total_length_ms, chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_name = f"{output_directory}/chunk{i//1000}_{(i + chunk_length_ms)//1000}.wav"
        chunk.export(chunk_name, format="wav")
        print(f"Exported {chunk_name}")

def transcribe_audio(file_path):
    with open(file_path, 'rb') as f:
        transcript = openai.Audio.transcribe("whisper-1", f, response_format="text")
    return transcript

def transcribe_directory(directory_path):
    transcripts = []
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".wav"): 
            file_path = os.path.join(directory_path, filename)
            print(f"Transcribing {filename}...")
            transcription = transcribe_audio(file_path)
            transcripts.append(transcription)
            # clean up audio chunk after it is transcribed
            os.remove(file_path)
    return " ".join(transcripts)

def generate_notes(model, transcription):
    # choose model to use
    if model == 'davinci':
        llm = OpenAI(model_name="text-davinci-003")
        prompt = PromptTemplate(
            input_variables=["transcription"],
            template="Take notes on the following text {transcription}. \n Respond with just the notes",
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        chunks = textwrap.wrap(transcription, 2000) 
        notes = list()
        for chunk in chunks:
            resp = chain.run(transcription=chunk)
            notes.append(resp)
        with open("notes.txt", 'a') as f:
            f.write("\n".join(notes))
        print(notes)
    else:        
        if model == 'gpt-3.5':
            llm = ChatOpenAI(model_name='gpt-3.5-turbo')
        elif model == 'gpt-4':
            llm = ChatOpenAI(model_name='gpt-4')

        text_prompt = """You will be provided with a transcription from a lecture/meeting/speech\
        Your task is to take detailed and nicely formatted notes on the information present in the transcription in order for someone to study from it \
        and not loose any of the important information from the transcription. Also add some review questions on the most important pieces of content \
        at the end. The transcription is: {text} 
        """  

        prompt = ChatPromptTemplate.from_template(text_prompt)

        chain = prompt | llm

        chunks = textwrap.wrap(transcription, 2000) 
        notes = list()
        for chunk in chunks:
            resp = chain.invoke({"text": chunk})
            notes.append(resp.content)
        with open("notes.txt", 'a') as f:
            f.write("\n".join(notes))
        print(notes)
        return notes

def main():
    parser = argparse.ArgumentParser(description='A Python script that does something.')
    parser.add_argument('--model', choices=['davinci', 'gpt-3.5', 'gpt-4'], type=str, help='choose model', default='davinci')
    args = parser.parse_args()
    output_filename = "speech.wav"
    try:
        record_audio.record_audio(filename=output_filename, device=1, samplerate=16000, channels=1, subtype='PCM_24')
    except Exception as e:
        print(f"An error occurred: {e}")
    audio_file= open(output_filename, "rb")
    output_directory = "audio_chunks"
    chunk_length_ms = 5 * 60 * 1000  # 10 minutes in milliseconds
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    split_audio(audio_file, output_directory, chunk_length_ms)

    transcription = transcribe_directory(output_directory)
    print(transcription)
    # delete audio file once we are done with it
    if os.path.exists(output_filename):
        os.remove(output_filename)

    generate_notes(args.model, transcription)        


if __name__ == "__main__":
    main()
