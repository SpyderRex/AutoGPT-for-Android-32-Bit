# AutoGPT for Android

I do much of my coding on Android, usually using the Termux app. However, there are certain things that cannot be used very well or at all in Termux, such as numpy or spacy. I tried to use the original version of AutoGPT on Termux, and I found that I cannot use such libraries as orjson and, most importantly, tiktoken, the token counter used in AutoGPT. I found a simpler version of AutoGPT and actually got it to work by modifying it in a few places: I got rid of orjson, tiktoken, spacy, and direct uses of numpy, all of which either cannot be installed in Termux or cannot be used properly in Termux. Instead of tiktoken as the token counter, I use nltk, which works fine on Termux. Then I realized I could make the same changes to the full AutoGPT project, and I have done so.

Typing commands in the terminal can be buggy at times on this program, but it is manageable.

You need both an OpenAI api key and a Pinecone api key to use the program. The original AutoGPT program has a variety of memory options to choose from, but I am narrowing it down to Pinecone. Pinecone does require numpy, but it can be installed with the command below. The OpenAI models cost a little to use, of course. You can create a free Pinecone account and get your api key. Store your OpenAI api key, your.Pinecone api key, and your Pinecone region in your .bashrc file as environment variables. 

If you are usking Termux, install numpy with:
```
pkg install python-numpy
```
Do this before you install the requirements, as pinecone-client requires numpy but you can't install numpy on Termux the usual way. I believe numpy is sometimes an issue with Userland as well.

Also, pillow is a requirement for the project, so you may need to install the following dependency first:

```
pkg install libjpeg-turbo
```

Install the requirements with:

```
pip3 install -r requirements.txt
```

And if you have trouble installing requests, try this first:

```
pkg install libxml2-dev libxslt-dev
```

Run the program with:

```
python3 -m autogpt
```

I have not tested any plugins or other features yet, but so far I have gotten the basics to work on Termux for Android.

Finally, if you have problems installing requirements or getting the program to work, let me know. Or do like I often do and use your greatest coding skill: copy and paste the error message into ChatGPT.
