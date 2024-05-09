Group: Asher Uman, Amanda Colby, Sarah Kam
Class: CSC290 Intro to AI

# English Language Generator

Context free grammar using a `State` object class to direct sentence generation

# Minmax Chessbot

Uses up to depth 3 to search for the optimal move and carry out. A little buggy

# Chinese Language Generator

This project is a rudimentary Chinese language generator. The sentences are mostly grammatically correct, if nonsensical. The grammar problems are analogous to English “a” versus “an” situations, where the part of speech is the same but the context requires it to be a specific choice – something that we can’t control in the terminal word choices without memory.

We constructed the grammar patterns based on resources from Smith’s CHI110 course, using three basic structures: a sentence form, and two question forms. The sentence form is

`ST -> NP + (intensifier | negate) + VP + NP + PERIOD`

This is a noun part, a modifier on the verb using an intensifier (e.g. “really” or “very”) or a negater (e.g. “not”), a verb part, another noun part, and a period.

We chose to only use verbs that apply to objects, like “she eats the apple” instead of “she swims” – she can’t swim an apple, in this case. This meant that we could always follow a verb part with a noun part (the object of the verb). We considered having two “types” of verbs, some that acted on objects and some that didn’t, but ultimately chose just this sentence form because it’s more interesting to represent in code.

For the first question form, we used the sentence structure and added the question-marker 吗. This is similar to saying “She’s your sister, right?” in English; “right?” turns the statement “She’s your sister” into a question. So the language generator has the option to turn any sentence into a question by tacking on the question-marker 吗 and adding a question mark.

For the second question form, we used a different common way of asking questions in Chinese, using the verb-negate-verb structure. This is like asking “Is she, or is she not, your sister?” We had to include a separate class of terminal words for this, because the verb must be the same in both parts (i.e. “swim not swim”, as opposed to “eat not swim”) and a context-free grammar has no memory, so it can’t reuse the same verb. After that, we constructed the grammar as follows:

`Q1 -> NP + verb-negate-verb + NP + question mark`

Because we used the same set of verbs that do actions on objects as in the previous part, we required that these verb-negate-verb structures were followed by a noun part, such as “Did she eat or not eat the apple?”
The individual sections of these sentences – NP (noun part), VP (verb part), ADJ (adjective), ADV (adverb) – are more similar to the English patterns.

Noun parts can have any number of adjectives, a preposition (possessive is used to apply it to the noun, grammatically), a noun, and the potential to attach more noun parts to the end.

`NP -> (ADJ)* + (preposition + possessive) + noun + (and + NP)*`

Verb parts have the verb, the option to make it past tense, the option to “soften” the impact of the verb (“she ate a little bit” vs “she ate”), and the option to add an adverb.

`VP -> verb + (past tense ) + (softener) + (ADV)`

Adjective parts have an optional intensifier (like “really” or “very”), an optional negater (“not”), the descriptor itself which is the actual adjective, and a possessive which in Chinese means that it is describing a noun.

`ADJ -> (intensifier) + (negate) + descriptor + possessive`

Adverb parts have an “adverbizer”, or a character to indicate that this phrase is describing a verb (kind of like “-ly” in English), an optional intensifier, an optional negater, and a descriptor. Note that the descriptors can be used similarly in both adjective parts and adverb parts, but the way they’re put together in a sentence differs grammatically.

`ADV -> adverbizer + (intensifier) + (negate) + descriptor`


We coded this using our infrastructure from the English language generator. We used the State object, which encodes whether or not a state is an accept state, and a dictionary containing what states it can lead to. Once we had the Chinese grammar patterns ready, we encoded them as finite state automata and linked those FSAs into a context-free grammar.
