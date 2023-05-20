# AutoGPT for Android

I do much of my coding on Android, usually using the Termux app. However, there are certain things that cannot be used very well or at all in Termux, such as numpy or spacy. I tried to use the original version of AutoGPT on Termux, and I found that I cannot use such libraries as orjson and, most importantly, tiktoken, the token counter used in AutoGPT. This has to do with Termux's aversion to Rust. I found a simpler version of AutoGPT and actually got it to work by modifying it in a few places: I got rid of orjson, tiktoken, spacy, and direct uses of numpy, all of which either cannot be installed in Termux or cannot be used properly in Termux. Instead of tiktoken as the token counter, I use nltk, which works fine on Termux. Then I realized I could make the same changes to the full AutoGPT project, and I have done so.

Typing commands in the terminal can be buggy at times on this program, but it is manageable.

You need both an OpenAI api key and a Pinecone api key to use the program. The original AutoGPT program has a variety of memory options to choose from, but I am narrowing it down to Pinecone. Pinecone does require numpy, but it can be installed with the command below. The OpenAI models cost a little to use, of course. You can create a free Pinecone account and get your api key. Store your OpenAI api key, your.Pinecone api key, and your Pinecone region in your .bashrc file as environment variables. I would suggest getting a Google api key and Google custom search engine id, since your IP address will most likely be blocked after so much web scraping.

If you are using Termux, run the following command before you do anything else:

```
./run.sh
```

This may or may not install all the necessary packages, depending on how your system is already set up.

This version of AutoGPT uses Firefox browser and geckodriver. I did this because Chromedriver doesn't have a 32 bit option, but Firefox and geckodriver do.

After all the requirements are installed, you can run the program with:

```
python3 -m autogpt
```

I have not tested any plugins or other features yet, but so far I have gotten the basics to work on Termux for Android.

Finally, if you have problems installing requirements or getting the program to work, let me know. Or do like I often do and use your greatest coding skill: copy and paste the error message into ChatGPT. Keep at it until you get everything working on Termux. I have it running on my 32 bit system, so if you are having trouble, it probably means some package is missing.
