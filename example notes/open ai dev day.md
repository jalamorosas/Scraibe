# Detailed Notes on OpenAI Dev Day Speech

## Introduction to OpenAI Dev Day
- First-ever OpenAI Dev Day.
- ChatGPT was launched about a year ago as a low-key research preview on November 30th.
- Success followed with the launch of GPT-4, the most capable AI model available.
- ChatGPT now has voice and vision capabilities.
- Dolly 3, the most advanced image model, was recently launched and is integrated within ChatGPT.
- ChatGPT Enterprise was introduced for business clients, featuring advanced security, privacy, and performance.

## Usage and Adoption
- Two million developers are using the OpenAI API across various applications.
- Over 92% of Fortune 500 companies use OpenAI products.
- ChatGPT has around 100 million weekly active users, achieved through organic growth.

## OpenAI's Market Position
- OpenAI is considered the most advanced and most widely used AI platform globally.

## Announcements and Updates

### GPT-4 Turbo
- Launch of a new model known as GPT-4 Turbo.

### Six Major Updates
1. **Extended Context Length**:
   - Original GPT-4 supported 8K tokens, sometimes extending to 32K.
   - GPT-4 Turbo expands to 128,000 tokens, equaling about 300 pages of a book.
   - Improved accuracy over long contexts.

2. **Enhanced Control**:
   - JSON mode for valid JSON responses.
   - Improved function calling, supporting multiple functions.
   - New feature for reproducible outputs via a 'C' parameter, offering consistent results.

3. **Updated World Knowledge**:
   - Retrieval feature to integrate external documents or databases.
   - Knowledge cutoff updated to April 2023.

4. **New Modalities**:
   - DALI 3, GPT-4 Turbo with Vision, and new text-to-speech models added to the API.
   - Text-to-speech with six preset voices demonstrated.
   - Whisper V3, an open-source speech recognition model, has been improved.

5. **Customization**:
   - Custom Models program launched for developing bespoke models with OpenAI's assistance.

6. **Increased Rate Limits**:
   - Token per minute rate doubled for established GPT-4 customers.
   - Introduction of Copyright Shield to protect customers against copyright infringement claims.

### Pricing Updates
- GPT-4 Turbo pricing significantly reduced.
- 1 cent per 1,000 prompt tokens, 3 cents per 1,000 completion tokens.
- New pricing results in a rate 2.75x cheaper than GPT-4.

### Partnership Acknowledgment
- Acknowledgment of a crucial partner in achieving these developments.

## Review Questions
1. What is the significance of the extended context length in GPT-4 Turbo, and how does it compare to the original GPT-4?
2. Describe at least two new features that provide developers with more control over the model's responses.
3. What is the purpose of the retrieval feature, and how does it improve GPT-4 Turbo's functionality?
4. How does the new text-to-speech model enhance user interaction, and what are its capabilities?
5. Explain the Custom Models program and its intended audience.
6. What is the function of the Copyright Shield, and to whom does it apply?
7. How has the pricing for GPT-4 Turbo changed, and what impact does this have for customers?
# Detailed Notes from Satya Nadella's Discussion and GPT-4 Announcement

## Microsoft's Partnership Outlook

### Satya Nadella on the Partnership

- **Appreciation for the Partnership**: Satya expresses a strong appreciation for the partnership with the unnamed partner, describing their work as "magical."
- **Infrastructure and Workloads**: He emphasizes the uniqueness of the infrastructure and workloads, which are synchronous, large, and data parallel.
- **Azure's Development**: Microsoft has been shaping Azure to support the partner's models by thinking from power to the data center (DC) to the rack to the accelerators to the network.
- **Goal for Microsoft**: Their primary goal is to build the best systems for the partner to enable them to create the best models and make these available to developers.

### Future of AI and the Partnership

- **Commitment to Excellence**: Microsoft is committed to ensuring that the partner has the best systems for training and inference and ample compute to continue advancing in AI.
- **Safety Priority**: Safety is a top priority from the beginning ("shift left on safety"), and Microsoft is focused on this aspect in partnership.

### Partnership Sentiment

- Satya Nadella believes they have the best partnership in tech and is excited about the prospect of building AGI (Artificial General Intelligence) together.

## ChatGPT and GPT-4 Improvements

### ChatGPT Enhancements

- **Introduction of GPT-4 Turbo**: ChatGPT now uses GPT-4 Turbo with the latest improvements, including the latest knowledge cutoff.
- **Web Browsing Capability**: ChatGPT can browse the web, which is live as of the announcement.
- **Extended Abilities**: It can write and run code, analyze data, take and generate images, among other tasks.
- **Model Picker Removal**: The model picker feature was removed based on user feedback to streamline the user experience.

### Vision for AI

- **AI as Agents**: The vision is to have AI that is smarter, more personal, customizable, and capable of performing tasks on behalf of the user.
- **Future of Computing**: The aim is to reach a point where users can ask the computer for what they need, and it will perform various tasks.

## Introduction of GPTs (Tailored ChatGPT)

### Concept of GPTs

- **Tailored Versions of ChatGPT**: GPTs are customized versions of ChatGPT designed for specific purposes.
- **Customization Features**: They come with instructions, expanded knowledge, and actions that can be published for others' use.

### Examples of GPTs

- **Canva's GPT**: Canva has created a GPT that allows users to start designing with natural language instructions.
- **Zapier's GPT**: Zapier's GPT enables actions across 6,000 applications, showcasing vast integration possibilities.

## Demo of GPT Live

### Jessica Hsieh's Presentation

- **Location of GPT**: GPT will reside in the upper left corner of the interface.
- **Zapier GPT in Action**: Jessica demonstrates asking GPT about her schedule, which prompts permission for data sharing and executes actions after permission is granted.
- **Identification of Schedule Conflicts**: The GPT identifies conflicts in the calendar and can notify contacts about schedule changes.

## GPT Store Launch

### Upcoming Launch

- **GPT Store**: A platform where GPTs can be listed and will feature the best and most popular ones.

### Review Questions

1. What are the two main aspects of the partnership that Satya Nadella highlighted with Microsoft's partner?
2. How has Microsoft shaped Azure to support the partner's AI models?
3. What are the new capabilities introduced with GPT-4 Turbo in ChatGPT?
4. What is the significance of safety in the partnership according to Satya Nadella?
5. What are GPTs and how do they integrate with existing applications, as shown by Canva and Zapier?
6. When is the GPT store expected to launch, and what purpose will it serve?
# Detailed Notes on GPT Store and Assistance API Presentation

## GPT Store

- **Policy Adherence**: GPTs must comply with store policies before becoming accessible.
- **Revenue Sharing**: Contributors of popular and useful GPTs will receive a portion of revenue.
- **Ecosystem Development**: The goal is to foster a vibrant ecosystem of GPTs.
- **Confidence in Growth**: Based on internal development, there is confidence in the potential for great contributions.

## Assistance API

- **Ease of Building**: The new API simplifies the creation of custom assistant experiences, which previously required significant time and engineering resources.
- **Features of the API**:
  - Persistent threads to handle long conversation histories.
  - Built-in retrieval capabilities.
  - Code interpreter with a working Python interpreter in a sandbox environment.
  - Improved function calling.

## Demonstration of Assistance API

- **Presented by**: Romain, head of developer experience.
- **New API Modalities**: The API now includes new features and an improved development experience.
- **Wanderlust Travel App Example**:
  - GPT-4 used for destination ideas.
  - Illustrations generated using DALI 3 API.
- **Adding an Assistant to the App**:
  - Simple process involving naming the assistant, setting initial instructions, and selecting a model (e.g., GPT-4 Turbo).
  - Code Interpreter and other tools can be enabled.
- **Assistant Functionality**:
  - Responds to queries within the app, such as providing top 10 things to do in a location.
  - Can annotate maps and interact with app features.

## Retrieval and Code Interpreter

- **Retrieval**: Allows the assistant to access and understand knowledge from various documents, such as PDFs.
- **Code Interpreter**: 
  - Enables AI to write and execute code on the fly.
  - Useful for complex calculations and tasks.
  - Demonstrated with a travel cost-sharing calculation.

## Developer Dashboard and Transparency

- Developers can track the assistant's steps, functions called, and document uploads in the developer dashboard.

## Conclusion and Future Outlook

- **API Beta Launch**: The Assistance API is now in beta.
- **Anticipated Evolution**: GPTs and assistants are expected to evolve into more capable agents that can plan and perform complex actions.
- **Importance of Early Adoption**: Encouragement for people to start using these agents to adapt to future advancements.
- **Continuous Improvement**: Commitment to updating systems based on user feedback.

---

# Review Questions

1. What must GPTs do before they are accessible in the GPT store?
2. How does the GPT store plan to incentivize the creation of useful GPTs?
3. What are the main features included in the new Assistance API?
4. What new capabilities were demonstrated using the Wanderlust travel app example?
5. How does the retrieval feature enhance the assistant's knowledge?
6. What is the purpose of the Code Interpreter within the Assistance API?
7. What can developers monitor through the developer dashboard?
8. What is the significance of early adoption of these new technologies as suggested in the presentation?
9. What is the company's approach to system updates and improvements?
# Detailed Lecture Notes on GPT Launch and Future Vision

## Introduction to GPTs
- Custom versions of chat GPT
- Combine instructions, extended knowledge, and actions

## Assistance API Launch
- Purpose: to facilitate the building of assistive experiences within user apps
- Significance: represents initial steps towards the development of AI agents
- Future prospects: capabilities of AI agents to be expanded over time

## GPT-4 Turbo Model
- Improvements:
  - Enhanced function calling
  - Expanded knowledge base
  - Lowered pricing for accessibility
  - Introduction of new modalities
- Overall: GPT-4 turbo model delivers improved performance and affordability

## Partnership with Microsoft
- Status: partnership is being deepened
- Implication: potential for greater integration and innovation

## AI's Impact on Society and Technology
- AI as a revolutionary force in technology and society
- Expected changes to be profound and multifaceted

## Empowerment Through AI
- Goal: to empower developers and creators
- Vision: to provide tools that enable significant contributions to society

## Intelligence Integration
- Future of AI: intelligence to be integrated ubiquitously
- Outcome: on-demand 'superpowers' for everyone

## Encouragement for Innovation
- The company's excitement for future creations with AI technology
- Anticipation for the architectural contributions to the new future by the community

## Looking Forward
- Comparison: today's launch will seem modest compared to future developments
- Ongoing work: creation of advanced tools for the community

## Closing Remarks
- Appreciation for the community's efforts
- Gratitude for attendance at the event

# Review Questions

1. What are the key features of the custom versions of chat GPT mentioned in the lecture?
2. What is the purpose of the Assistance API, and what does it signify in the context of AI development?
3. List the improvements introduced with the GPT-4 turbo model.
4. How is the partnership with Microsoft expected to influence the development and use of AI?
5. Why does the speaker believe AI will be a technological and societal revolution?
6. What future vision does the speaker have for the integration of AI in everyday life?
7. How does the company view the potential of AI to empower individuals and the community?
8. What does the speaker suggest about the current developments in comparison to what is planned for the future?
9. What sentiments are expressed in the closing remarks of the lecture?