## Markov Poet
-----------

<p align="left"><em>
red hearts flying<br />
deep with the chatter of day
</em></p>


<p align="center"><em>
walking home to the photo<br />
the sound<br />
upon red rocks
</em></p>


<p align="right"><em>organ reedy as the highway<br />
in twisted tapers with a winter solstice moon<br />
under a broken bone of night sky<br />
dreams of friends reunited
</em></p>

-----

Markov Poet is a poetry generator based on a Markov chain that simulates poetic line breaks by including a new line token in its model.


### Usage

```python
markov = Markov()

markov.add_file("corpus.txt")

haiku = """the piano room
pure ivory keys
under a layer of dust"""
markov.add_poem(haiku)

lines = ['old pond', 'frog leaping', 'splash']
markov.add_lines(lines)

# randomness optional and generally not recommended
randomness = 0.2
generator = markov.generator(randomness)
generator.generate_line()

number_of_lines = 7
print(generator.generate_formatted(number_of_lines))
```

Also included is a demo driver.

```bash
$ python3 demo.py [-h] [-f FILENAME] [-r RANDOMNESS] [-n NUMBER]
```

#### Options
- **-f** filename: specify the name of a file to read as the reference corpus. The expected format is of plain text. The model tokenizes words and line breaks but will ignore other white space.
- **-r** randomness (between 0.0 and 1.0): introduce an element of randomness into the generation. At 1.0, the chain is ignored and every word is randomly selected from the language. 
- **-n** number: specify the number of poems to output.
