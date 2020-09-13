import torch
from tkinter import *
from tkinter.ttk import *
from tkinter import font
from tkinter.filedialog import askopenfilename
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM

# set text index
idx = 0
bottom = None

text = (
    (
        "A vacation is when you take a trip to a _. place with your "
        "_. family. Usually you go to some place that is near a _. or up "
        "on a _. . A good vacation is one where you can ride _. or play _. "
        "or go hunting for _. I like to spend my time _. or _. . When "
        "parents go on vacation, they spend their time eating three _. a day, "
        "and fathers play golf, and mothers sit around _. all day"
    ),
    (
        "I can't believe its already _.  I can't wait to put on  "
        "my _. and visit every _. in my neighborhood.  This year, I "
        "am going to dress up as (a) _. with __.  Before I _. , "
        " I make sure to grab my _. _. to hold all of my _. . "
        "Finally, all of my _. are ready to go! When _. answers the door, "
        "I say, _. or Treat  Yum! I got (a) _. and (a) _. .  We "
        "visit _. houses and decide it's time to _. home.  My _. "
        "says if I eat too much _. , my stomach will _. , so I'll eat "
        "just _. pieces  and go straight to bed.  I hope I'll  have _. "
        "dreams for _. tonight!  Happy _."
    ),
    (
        "Shall I _. thee to a summer’s _. ? "
        "Thou art more _. and more temperate _. "
        " winds do shake the darling buds of _.  "
        "And summer’s lease hath all too short a date; "
        "Sometime too _. the eye of heaven shines, "
        "And often is his gold _. dimm'd; "
        "And every _. from fair sometime declines, "
        "By chance or nature’s changing _. untrimm'd; "
        "But thy _. summer shall not fade, "
        "Nor _. possession of that fair thou ow’st; "
        "Nor shall _. brag thou wander’st in his shade, "
        "When in eternal _. to time thou grow’st: "
        "So long as men can _. or eyes can see, "
        "So long lives this, and this gives _. to thee."
    ),
    (
        "Four score and _. years ago our fathers brought forth on this _. , a new "
        "_. , conceived in Liberty, and dedicated to the _. that all men are "
        "created _.  Now we are _. in a great civil war, _. whether that nation "
        ", or any nation so _. and so dedicated, can _. endure. We are met on a "
        "great _. of that war. We have come to dedicate a _. of that field, "
        "as a final resting place for _. who here gave their lives that _. nation "
        "might live. It is _. fitting and proper that we should do this."
    ),
    (
        "Today I went to the zoo. I saw a large _. jumping up and down in its tree."
        "He _. through the large tunnel that led to its _. /.  I got some peanuts "
        "and passed them through the cage to a gigantic gray _. towering above my "
        "head.  Feeding that animal made me hungry.  I went to get a _. scoop of "
        "ice cream. It filled my stomach.  Afterwards I had to _. so _. to catch our bus. "
        "When I got home I _. tired. My mom _. me about my day at the _. . "
    ),
    (
        "My Day at the Fun Park From camp my fabulous group went to a _. "
        " amusement park. It was a fun "
        "park with lots of cool _. and enjoyable "
        "play structures. When we got there my annoying counselor "
        "shouted loudly, Everybody off the _. We "
        "all pushed out in a terrible hurry. My counselor handed out the "
        "yellow tickets, and we scurried in. I was so excited, I couldn't "
        "figure out what exciting thing to do first. I saw a scary roller "
        "coaster I really liked so I _. ran over to get "
        "in the long line that had about _. people in "
        "it. When I finally got on the roller coaster I was _. "
        " . In fact I was so nervous my two knees were "
        "knocking together. This was the _. "
        "ride I had ever been on! In about two minutes Crank ! went the "
        "grinding of the gears, and the ride began! When I got to the "
        "bottom I was a little _.  but I was "
        "proud of myself. The rest of the day went _. "
        " It was a _. day at the fun park. "
    )
)


def NewFile():
    print("New File!")


def OpenFile():
    name = askopenfilename()
    print(name)


def About():
    print("This is a simple example of a menu")


def predict():
    global bottom
    # Acknowledgment
    # Article: A.I. Plays Mad Libs and the Results are Terrifying
    # Taken From: https://towardsdatascience.com/a-i-plays-mad-libs-and-the-results-are-terrifying-78fa44e7f04e

    # start the progess bar
    progress_bar.start()
    # run_progressBar()

    # Load pre-trained model with masked language model head
    bert_version = 'bert-large-uncased'
    # bert_version = 'bert-large-cased'
    model = BertForMaskedLM.from_pretrained(bert_version)

    # Preprocess text
    tokenizer = BertTokenizer.from_pretrained(bert_version)
    tokenized_text = tokenizer.tokenize(text[idx])
    mask_positions = []
    for i in range(len(tokenized_text)):
        if tokenized_text[i] == '_':
            tokenized_text[i] = '[MASK]'
            mask_positions.append(i)

    # Predict missing words from left to right
    model.eval()
    for mask_pos in mask_positions:
        # Convert tokens to vocab indices
        token_ids = tokenizer.convert_tokens_to_ids(tokenized_text)
        tokens_tensor = torch.tensor([token_ids])
        # Call BERT to predict token at this position
        predictions = model(tokens_tensor)[0, mask_pos]
        predicted_index = torch.argmax(predictions).item()
        predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]
        # Update text
        tokenized_text[mask_pos] = predicted_token

    for mask_pos in mask_positions:
        tokenized_text[mask_pos] = "_" + tokenized_text[mask_pos] + "_"
    # print(' '.join(tokenized_text).replace(' ##', ''))
    madlib = (' '.join(tokenized_text).replace(' ##', ''))

    # terminate the progress bar
    progress_bar.stop()

    bottom.delete(1.0, END)
    bottom.insert(END, madlib)
    bottom.pack()

    status['text'] = "Story Generation Successful"


# run the progress bar
def run_progressBar(self):
    progress_bar['maximum'] = 100

    for i in range(101):
        time.sleep(0.05)
        progress_bar["value"] = i
        progress_bar.update()

    progress_bar["value"] = 0


def getAStory():
    global idx
    global bottom
    global numOfStories
    idx += 1
    if idx > len(text) - 1:
        idx = 0

    top.config(state=NORMAL)
    top.delete(1.0, END)
    top.insert(END, text[idx])
    # top.pack(fill=BOTH, expand=True)
    top.pack()

    numOfStories['text'] = "Story " + str(idx + 1) + " of " + str(len(text))
    bottom.delete(1.0, END)

    # clear status bar
    status['text'] = ""


def clearScreen():
    top.delete("1.0", "end")
    bottom.delete("1.0", "end")

    # clear status bar
    status['text'] = ""


# set up main window
root = Tk()
menu = Menu(root)
root.config(menu=menu)
root.title('Reverse Mad Libs')
root.iconbitmap('William_Shakespeare.ico')
root.geometry("800x550")
root['background'] = '#808080'

# Set up the menu
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

# set up orginal story frame
originalframe = LabelFrame(root, text="Original Story")
originalframe.pack(fill="both", expand="yes")
vscrollbar = Scrollbar(originalframe, orient=VERTICAL)
vscrollbar.pack(fill=Y, side=RIGHT)
top = Text(originalframe, height=10, width=50, wrap=WORD)
top.configure(font=("Times New Roman", 18, "bold"))
top.insert(END, text[idx])
# top.pack()

top.pack(fill=BOTH, expand=True)

getButton = Button(originalframe, text="Get a Story", command=getAStory)
getButton.pack(side=LEFT)
genButton = Button(originalframe, text="Generate", command=predict)
genButton.pack(side=LEFT, padx=5, pady=5)
clrButton = Button(originalframe, text="Clear", command=clearScreen)
clrButton.pack(side=LEFT, padx=5, pady=5)

# Progress bar widget
progress_bar = Progressbar(originalframe, orient=HORIZONTAL, style='black.Horizontal.TProgressbar',
                           length=475, mode='indeterminate')
progress_bar.pack(pady=10)

# set up mad lib story frame
madlibsframe = LabelFrame(root, text="Madlibs Story")
madlibsframe.pack(fill="both", expand="yes")
vscrollbar = Scrollbar(madlibsframe, orient=VERTICAL)
vscrollbar.pack(fill=Y, side=RIGHT)
bottom = Text(madlibsframe, height=10, width=50, wrap=WORD, state=NORMAL)
bottom.configure(font=("Times New Roman", 18, "bold"))

closeButton = Button(root, text="Close", command=root.quit)
closeButton.pack(side=RIGHT, padx=5, pady=5)
numOfStories = Label(root, text="Story " + str(idx + 1) + " of " + str(len(text)), borderwidth=2, relief=SUNKEN)
numOfStories.pack(side=RIGHT, padx=5, pady=5)
status = Label(root, text="", width=500, borderwidth=2, relief=SUNKEN)
status.pack(side=RIGHT, padx=5, pady=5)

mainloop()
