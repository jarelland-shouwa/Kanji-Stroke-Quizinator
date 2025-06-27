# Kanji Stroke Quizinator
#### Video Demo: https://youtu.be/C9LE3p8u09Y
#### Description:
# How to run this project
In Terminal,
1. execute ```pip install -r requirements.txt``` to install required packages
2. run the project by executing ```py project.py```

# Introduction
**Kanji** is one of the three orthographies of the Japanese language (<ruby><rb>日</rb><rt>に</rt> <rb>本</rb><rt>ほん</rt> <rb>語</rb><rt>ご</rt></ruby>). Learning kanji comes with learning how to read them, and how to write them, with this project focused on the order each stroke is written (i.e. *stroke order*, <ruby><rb>筆順</rb><rt>ひつじゅん</rt></ruby>). Stroke order is important because it ensures the kanji is written beautifully and is a standard learnt by Japanese people in their education system. The knowledge of kanji is so important that there is an examination board in Japan that administers the [Japan Kanji Aptitude Test「<ruby><rb>日本漢字能力検定</rb><rt>にほんかんじのうりょくけんてい</rt></ruby>」](https://www.kanken.or.jp/kanken/), AKA the Kanken (<ruby><rb>漢検</rb><rt>かんけん</rt></ruby>). This test evaluates one's knowledge of kanji, like readings and meanings. Particularly, stroke order is tested from level 10 to 5. Hence, I thought of this simple mini app that allows anyone to just test their stroke order knowledge without pen and paper.

# Project explanation
## Stroke positions
At first, I thought this app would be hard to accomplish as I would need to somehow obtain not only the *stroke order of a kanji*, but also *where* in the character to place the stroke's annotation. Fortunately, there is a resource online (see [Attribution](#attribution)) that provides data-rich *svg files* for practically every kanji from Kanken level 10 to 5. And I think this is the most interesting aspect of this project. Each svg file contains each **stroke's number**, **x-** and **y- coordinate positions**.

**.svg file example (04eab.svg) (享):**
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="109" height="109" viewBox="0 0 109 109">
...
<g id="kvg:StrokeNumbers_04eab" style="font-size:8;fill:#808080">
	<text transform="matrix(1 0 0 1 44.25 9.50)">1</text> <!-- (1 0 0 1 44.25 9.50) is an example of the match the re is looking for-->
	<text transform="matrix(1 0 0 1 13.50 23.50)">2</text>
	<text transform="matrix(1 0 0 1 28.50 39.13)">3</text>
	<text transform="matrix(1 0 0 1 39.75 30.13)">4</text>
	<text transform="matrix(1 0 0 1 44.50 43.50)">5</text>
	<text transform="matrix(1 0 0 1 29.25 59.98)">6</text>
	<text transform="matrix(1 0 0 1 48.50 70.50)">7</text>
	<text transform="matrix(1 0 0 1 11.25 79.63)">8</text>
</g>
</svg>
```

Knowing this, I can read the svg file and extract the relevant information. Using a regular expression to do so, I can find a match with the format required, capture the positions for one stroke, slice off the text that had already been seen, then repeat this until there are no more matches.

**Python code snippet (from the UDF ```obtain_stroke_x_y_position```) that obtains the coordinates of each stroke's position**
```py
stroke_number = 1
stroke_x_y_position_dict = dict()
while "transform" in source_text:
    matches = re.search(r"(\(1 0 0 1 (\d+\.?\d*\d*) (\d+\.?\d*\d*)\))+", source_text)
    stroke_x_y_position_dict[stroke_number] = [float(matches[2]), float(matches[3])] # x-, y- coordinates
    i = source_text.index(matches[0])
    source_text = source_text[i+len(matches[1]):] # cuts off text that a match has been found previously
    stroke_number += 1
```

## Modes
The app's foundation was built using the Pythonic tkinter module. There are *two* modes for the app:
1. Practice
> Practice mode allows for multiple tries and if the user wants to give up on a question, it is possible to skip to the next question. The mode also does not generate a score for user at the end.
2. Quiz
> Quiz mode does *not* allow for multiple tries, so whichever the outcome of an answer, the user has to move onto the next question. The mode generates a score at the end of the quiz. It also awards a corresponding "grade" that [Japanese schools typically use](https://en.wikipedia.org/wiki/Academic_grading_in_Japan).

## Features
There are 4 buttons in the question frame:
1. Check
2. Reset
> Resets the order of stroke buttons clicked.
3. Undo
> Undos the latest storke button clicked.
4. Next/Skip
> *Skip* only appears when the user fails to answer a question correctly in Practice mode.

## Results page
This frame shows which kanjis were answered correctly and wrongly, along with a button that when clicked, shows the *correct stroke order* and the *user's attempt*.

For Quiz mode, as mentioned above, a score, grade, and an appropriate Japanese comment is displayed. Also, instead of ticks (✓) for a correct answer, I opted for its [Japanese equivalent](https://en.wikipedia.org/wiki/O_mark) (⭕️).

# Files
## project.py
This file essentially runs ```main()```, which creates an instance of the ```App``` class.

## app_classes.py
This file contains the classes of the frames and widgets that make of the app.

# Attribution
For the Kanjis found in each Kanken (漢検「日本漢字能力検定」) level, I obtained them from [Nihongo-Pro](https://www.nihongo-pro.com/kanji-pal/list/kanken).

For the Kanji SVG images and stroke annotation positions, I used data from [KanjiVG](https://kanjivg.tagaini.net/) by Ulrich Apel, licensed under CC BY-SA 3.0.