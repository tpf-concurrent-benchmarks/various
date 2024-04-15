# Generates an input.txt file with random text

determiners = ["The", "Another", "Some", "Any", "This", "That", "The only", "A uniquely"  ]
determiners_plural = ["The", "Some", "Any", "These", "Those", "Several", "Many"]

adjectives = ["quick", "lazy", "sleepy", "noisy", "hungry",
              "thirsty", "fat", "skinny", "happy", "sad",
              "angry", "scared", "brave", "cowardly"]

# Nouns
animals = ["fox", "dog", "elephant", "kangaroo", "rhino",
           "lion", "tiger", "bear", "wolf", "whale", "shark",
            "fish", "bird", "cat", "mouse", "rabbit", "turtle",
            "snake", "lizard", "monkey", "ape", "human", "alien",
]
animals_plural = ["foxes", "dogs", "elephants", "kangaroos", "rhinos",
                  "lions", "tigers", "bears", "wolves", "whales", "sharks",
                  "fish", "birds", "cats", "mice", "rabbits", "turtles",
                  "snakes", "lizards", "monkeys", "apes", "humans", "aliens",
]

verbs = ["jumps", "lifts", "bites", "licks", "pats", "drives",
          "travels", "walks", "jogs", "runs", "swims", "flies", "crawls",
          "skips", "hops", "runs", "hops", "dances", "sings", "laughs",
          "cries", "sleeps", "eats", "drinks", "plays", "reads", "writes"]
verbs_plural = ["jump", "lift", "bite", "lick", "pat", "drive",
                "travel", "walk", "jog", "run", "swim", "fly", "crawl",
                "skip", "hop", "run", "hop", "dance", "sing", "laugh",
                "cry", "sleep", "eat", "drink", "play", "read", "write"]

adverbs = ["quickly", "lazily", "sleepily", "noisily", "hungrily",
           "thirstily", "happily", "sadly", "angrily",
            "bravely", "cowardly", "loudly", "softly", "slowly", "fast",
]


import random

random.seed(42)

def sentence():
  is_plural = random.choice([True, False])
  
  if is_plural:
    determiner = random.choice(determiners_plural)
    animal = random.choice(animals_plural)
    verb = random.choice(verbs_plural)
  else:
    determiner = random.choice(determiners)
    animal = random.choice(animals)
    verb = random.choice(verbs)
    
  adjective = random.choice(adjectives)
  adverb = random.choice(adverbs)
  
  return f"{determiner} {adjective} {animal} {verb} {adverb}."

def paragraph():
  num_sentences = random.randint(3, 7)
  return " ".join([sentence() for _ in range(num_sentences)])

def text(paragraphs = 50*10**6, max_size = 4.3*10**9, fileName = "input.txt"):
  bytes_written = 0
  with open(fileName, "w") as file:
    for _ in range(paragraphs):
      par = paragraph() + "\n\n"
      file.write(par)
      bytes_written += len(par)
      if (bytes_written > max_size):
        break

      
text()