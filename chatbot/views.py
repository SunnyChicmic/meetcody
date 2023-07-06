import os
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import View
from langchain import OpenAI,PromptTemplate,LLMChain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
import textwrap
import re

openai_api_key='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'


def generate_response(txt):
    # Instantiate the LLM model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    # Split text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]
    # Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)



def summarizer(request): #brute force appraoch
    #summarizer method
    if request.method=='POST':
        text_data=request.POST['text_input']
        response=generate_response(text_data)
        return render(request,'index.html',{'res':response,'flag':1})
    return render(request,'index.html',{"flag":0})




def summarizer_with_prompt(request):
    if request.method=='POST':
        text_data=request.POST['text_input']
        #implemention 
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        # Split text
        text_splitter = CharacterTextSplitter()
        texts=text_splitter.split_text(text_data)
        docs = [Document(page_content=t) for t in texts]
        
        
        prompt_template = """Write a concise bullet point summary of the following:
                            {text}
                            CONSCISE SUMMARY IN BULLET POINTS:"""

        BULLET_POINT_PROMPT = PromptTemplate(template=prompt_template,
                                input_variables=["text"])
        # prompt=BULLET_POINT_PROMPT
        
        
        chain = load_summarize_chain(llm, 
                             chain_type="stuff",
                             prompt=BULLET_POINT_PROMPT
                             )
        
        response=chain.run(docs)
        
        response= textwrap.fill(response,width=100,break_long_words=False,
                             replace_whitespace=False)
        response=re.sub(r'\n+', '', response) #regex to remove extra new lines
        response=response.strip().split('•')
        response=[x.strip() for x in response if x.strip() != ""]
        return render(request,'index.html',{'res':response,'flag':1})
    return render(request,'index.html',{"flag":0})
    
    
    
    

# def chatbot(request):
#         if request.method=="POST":
            
#         return render(request,'index.html',{'res':response,'flag':1})
#     return render(request,'index.html',{"flag":0})


