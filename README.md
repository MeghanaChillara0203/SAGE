# **SAGE: AI-Powered Sustainability Chatbot**  

SAGE (**Sustainable Advisory & Guidance Expert**) is an **AI-powered chatbot** designed to provide intelligent insights on sustainability. This project features **two versions** of SAGE:  

- **DistilBERT-Based Chatbot:** Utilizes **intent recognition and NLP** for structured responses.  
- **GPT-Powered Chatbot:** Leverages **OpenAI’s GPT-3.5 API** to generate dynamic, context-aware answers.  

By comparing both versions, we analyze their **accuracy, response quality, and effectiveness** in aiding sustainability decision-making.  

🌍 Whether you're exploring **eco-friendly solutions**, **carbon footprints**, or **sustainable lifestyle choices**, SAGE has you covered!  

---

## **Setup & Requirements**  

### **Prerequisites**  
Ensure you have the following dependencies installed:  

If you're using Conda, create or update your environment:

```bash
conda env create -f requirements.yml  # For new environment
conda env update --file requirements.yml --prune  # Update existing environment
```

If you only want to install via pip, use:

```bash
pip install -r <(echo "$(sed 's/- /--/' requirements.yml | sed 's/^dependencies:/ /g' | sed 's/pip:/ /g')")
```

**📌 Ensure you have an OpenAI API Key for GPT Mode!**  
To use the **GPT-powered chatbot**, create an **API key** from OpenAI's website:  

🔗 **Visit:** [https://platform.openai.com/signup/](https://platform.openai.com/signup/)  
📌 **Copy your API Key and replace it in the `GPT_GUI.py` file**  

```python
openai.api_key = 'your-api-key-here'  # Replace this with your actual API key
```

---

## **How to Compile & Run SAGE**  

### **Running the Chatbot with OpenAI API**  
For an all-in-one execution, use:  
```bash
make all
```

### **Step-by-Step Execution**  

#### **1️⃣ Train the DistilBERT Chatbot**  
Before running SAGE, train the NLP-based chatbot:  
```bash
make train
```

#### **2️⃣ Launch the DistilBERT Chatbot**  
Once trained, start the interactive chatbot:  
```bash
make chat
```

#### **3️⃣ Use the GPT-Powered Chatbot**  
To test the **ChatGPT-enhanced** version of SAGE:  
```bash
make gptui
```

---

## **How SAGE Works**  

SAGE operates in two modes:  

### 🔹 **DistilBERT Chatbot:**  
- Loads a **pre-trained model** and predefined **intent-response pairs**.  
- Uses NLP classification to **predict user intent** and generate responses.  
- Provides **structured, rule-based answers**.  

### 🔹 **GPT-Powered Chatbot:**  
- Uses **OpenAI’s GPT-3.5 API** to process natural language queries.  
- Generates **context-aware, dynamic responses** based on user input.  
- Enhances conversation flow with **AI-driven reasoning and deeper insights**.  

By comparing the two models, SAGE explores the advantages of **rule-based AI** vs. **deep learning-based conversational AI** in addressing **sustainability queries**.  

---

## **User Experience & Expected Output**  

🖥️ **Graphical Interface:**  
- A **user-friendly** chatbot window  

💬 **Interacting with SAGE:**  
- **Type a question & hit enter** → Your query disappears, and SAGE provides an AI-generated response.  
- **Click "Exit"** → The chatbot closes gracefully.  

**🤖 GPT Mode Features:**  
- Handles **complex and open-ended queries** better than the DistilBERT model.  
- Generates **long-form, contextual answers** based on AI training data.  
- Uses **real-time GPT interaction** instead of predefined responses.  

---

## **Key Insights & Findings**  

📌 **Comparison of DistilBERT & GPT Models**  

| Feature                  | DistilBERT Chatbot | GPT-3.5 Chatbot |
|--------------------------|-------------------|-----------------|
| **Response Type**        | Rule-based        | Contextual & Dynamic |
| **Accuracy**             | High for structured queries | Adaptive & evolving |
| **Training Needed?**     | Yes (pre-trained NLP model) | No (API-based AI) |
| **Best Use Case**        | Quick predefined answers | Deep, AI-driven explanations |

🎯 **SAGE in Action:**  
- 🟢 **Answered sustainability queries** effectively using **both AI techniques**.  
- 🟢 **Compared response accuracy & quality** through user testing.  
- 🟢 **Validated AI's role in sustainability guidance** by analyzing user interactions.  

---

## **Why SAGE Matters**  
- 🌍 **Sustainability-Focused:** AI-powered insights on eco-friendly solutions.  
- 🤖 **Machine Learning at Work:** Combines **intent recognition, NLP, and GPT AI** for better understanding.  
- 🎯 **User-Centric Design:** A clean, intuitive chatbot experience with **two AI models for comparison**.  

SAGE is more than just a chatbot—it’s a demonstration of **AI’s evolving role in sustainability education and decision-making**. 🌱💡  

---

### **📸 Screenshots of SAGE**  

#### 1️⃣ **DistilBERT Chatbot Interface**  
![DistilBERT Chatbot](figs/sagechatbot.png)  

#### 2️⃣ **GPT-Powered Chatbot Interface**  
![GPT Chatbot](figs/gptchatbot.png)  

#### 3️⃣ **Comparison: GPT vs. DistilBERT Responses**  
![GPT vs AI Chatbot](figs/sagevsgpt.png)  

---

🔹 **Ready to explore AI-driven sustainability? Run SAGE today!** 🚀  

---

#### **Authors:** Meghana Chillara, Zach Nichols, Tina Puzzo  
📅 **Date:** April 2023  

