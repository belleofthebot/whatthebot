# -*- coding: utf-8 -*-
import json, statistics

data = [
{
 "key": "synthetic-media",
 "correct": "No evidence it changed any result, alongside real second order harms",
 "distractors": [
   "Clear evidence that AI fakes decided several national election results",
   "That almost no AI generated content circulated during either campaign",
   "That AI content displaced most conventional campaign advertising"
 ],
 "note": "No result was shown to have been changed; AI content did circulate widely; it stayed a small share of campaign material."
},
{
 "key": "system-prompt",
 "correct": "A block of instructions the company sets before your conversation",
 "distractors": [
   "The first thing the user types at the start of a new conversation",
   "A running summary of the conversation that the model writes itself",
   "A diagnostic message the operating system prints when a program starts"
 ],
 "note": "The system prompt is in place before the user's first message, is written by the provider rather than by the model, and has nothing to do with the operating system."
},
{
 "key": "taboo-your-words",
 "correct": "Swapping it for what it stands for, and arguing about that instead",
 "distractors": [
   "Agreeing on one official definition, and holding every speaker to it",
   "Refusing to discuss the topic until the term has been defined properly",
   "Barring the word from polite conversation because it causes offence"
 ],
 "note": "Tabooing replaces the word rather than defining it, and it continues the argument rather than deferring or avoiding it; offence is not the point."
},
{
 "key": "teacher-ai",
 "correct": "Training a smaller model to copy the outputs of a larger one",
 "distractors": [
   "Removing duplicated and biased examples from training data",
   "Compressing a trained model so it takes up less disk space",
   "Filtering a model's answers at run time to block bad ones"
 ],
 "note": "Those describe data cleaning, quantisation and output filtering; none involves a student model learning from a teacher's outputs."
},
{
 "key": "temperature",
 "correct": "It samples from a distribution, and temperature sets how adventurously",
 "distractors": [
   "It learns from each exchange, so its answers drift as you keep talking",
   "It has a fixed error rate, and some share of answers come out wrong",
   "The reply is assembled from cached answers to earlier similar prompts"
 ],
 "note": "The weights do not change during use, the variation is deliberate sampling rather than error, and replies are generated fresh rather than fetched from a cache."
},
{
 "key": "tokens",
 "correct": "Text arrives split into tokens, and letters inside one are invisible",
 "distractors": [
   "It reads only the first and last few characters of every word it sees",
   "It guesses at the count whenever a reply is taking too long to compute",
   "Whole numbers above ten are stored imprecisely inside the model itself"
 ],
 "note": "The whole token is read rather than its edges, there is no time budget that triggers guessing, and numbers are not held as imprecise quantities."
},
{
 "key": "toner",
 "correct": "Self governance cannot withstand the pressure of the profit motive",
 "distractors": [
   "Frontier development should be halted until alignment is solved first",
   "The board had been misled about the company's revenue figures",
   "Altman should be barred from leading any AI company ever again"
 ],
 "note": "Their Economist piece argued for outside regulation rather than a halt, made no claim about revenue figures, and asked for no personal ban."
},
{
 "key": "training-run",
 "correct": "A single enormous computation, after which the weights are fixed",
 "distractors": [
   "A continuous process, updating weights as people use the model",
   "A series of small daily updates rolled out to the live model",
   "A separate computation carried out for each corporate customer"
 ],
 "note": "A run ends and the weights stop moving; use does not update them, there is no daily retraining, and one run serves every customer."
},
{
 "key": "transformer",
 "correct": "Weigh how much every part of the input matters to every other part",
 "distractors": [
   "Run on graphics cards, which earlier architectures could not exploit",
   "Carry memory of earlier conversations from one session to the next",
   "Fetch pages from the open internet while a reply is being composed"
 ],
 "note": "Earlier architectures also ran on GPUs; attention works inside a single input, carries nothing between sessions and retrieves nothing from the web."
},
{
 "key": "ubi",
 "correct": "Fell slightly: 1.3 hours a week, and earned income by 1,800 dollars",
 "distractors": [
   "Rose sharply: 4 hours a week, and earned income by 3,000 dollars",
   "Held steady: within 0.1 hours a week, and earned income unchanged",
   "Fell steeply: 9 hours a week, and earned income by 12,000 dollars"
 ],
 "note": "The measured fall was small but clearly not zero, so there was no rise, no flat result and no collapse in hours."
},
{
 "key": "value-lock-in",
 "correct": "One set of values becomes permanent, with no way left to change it",
 "distractors": [
   "An AI system develops values of its own and starts acting on them",
   "Different countries settle on incompatible rules for AI development",
   "Companies write their own ethics policies instead of following the law"
 ],
 "note": "Those name misalignment, regulatory fragmentation and self regulation; lock-in is about permanence, whoever's values are the ones locked in."
},
{
 "key": "weight-security",
 "correct": "Defending against top tier nation state attack is not yet possible",
 "distractors": [
   "Current security at the leading labs is already adequate against them",
   "Weights cannot be exfiltrated, because the files are too large",
   "Frontier model weights have already been stolen on several occasions"
 ],
 "note": "RAND found current security short of the top threat tier, treated theft as feasible at every level it examined, and recorded no repeated thefts."
},
{
 "key": "weights",
 "correct": "Billions of numbers set by training, which nobody chose one by one",
 "distractors": [
   "The set of rules its engineers wrote out and ranked in priority order",
   "The training data itself, held inside the model and looked up on demand",
   "A record of its past conversations, kept so that the model improves"
 ],
 "note": "Weights are not hand written rules, they are not a stored copy of the training data, and they do not accumulate from conversations."
},
{
 "key": "who-gives-a-number",
 "correct": "Dario Amodei, at Anthropic",
 "distractors": [
   "Demis Hassabis, at DeepMind",
   "Yann LeCun, formerly at Meta",
   "Jensen Huang, at Nvidia"
 ],
 "note": "Amodei has publicly put catastrophe at about 25 percent; the other three have declined to attach any number."
},
{
 "key": "who-makes-the-chips",
 "correct": "Outside foundries, chiefly TSMC in Taiwan",
 "distractors": [
   "Nvidia itself, at its own fabs in California",
   "A consortium of American chip manufacturers",
   "Its cloud customers, Microsoft and Amazon"
 ],
 "note": "Nvidia is fabless and owns no plants; no American consortium and no cloud provider fabricates its chips."
},
{
 "key": "who-owns-it",
 "correct": "Never disclosed, by either company or by Anthropic",
 "distractors": [
   "Published in full in each company's annual report",
   "Fixed at ten percent each, under a written agreement",
   "Held in trust and voted by an independent board"
 ],
 "note": "No percentage has ever been published by any of the three parties, and no such cap or trust arrangement has been announced."
},
{
 "key": "xai",
 "correct": "Exists, and is shorter, benchmark based and permissively worded",
 "distractors": [
   "Does not exist, unlike the published frameworks of its peers",
   "Exists, and is made legally binding by a signed agreement",
   "Exists, and is written and enforced by an outside auditor"
 ],
 "note": "The framework is published, is voluntary rather than binding, and is written in house rather than by an auditor."
},
{
 "key": "yang",
 "correct": "A thousand dollars a month to every American adult, funded by a value added tax",
 "distractors": [
   "A guaranteed federal job at fifteen dollars an hour for anyone displaced by automation",
   "A tax of five thousand dollars a year on every industrial robot installed",
   "Two years of free retraining, paid for by a levy on large technology firms"
 ],
 "note": "The Freedom Dividend was unconditional cash to everyone; Yang proposed no job guarantee, no robot tax and no retraining scheme in its place."
},
]

src = json.load(open('/tmp/opts_5.json'))
assert [e['key'] for e in src] == [e['key'] for e in data]

ranks = []
bad = []
for e in data:
    opts = [e['correct']] + e['distractors']
    L = [len(o) for o in opts]
    ratio = max(L) / min(L)
    rank = sorted(L, reverse=True).index(len(e['correct'])) + 1
    ranks.append(rank)
    flag = []
    if ratio > 1.25: flag.append('SPREAD %.2f' % ratio)
    if len(set(opts)) != 4: flag.append('DUP')
    if any(c in ''.join(opts) for c in ['&', '<', '>', '’', '"', '!']): flag.append('CHARS')
    print('%-20s %-2s %s  spread %.2f rank %d %s' % (e['key'], 'ok' if not flag else '!!', L, ratio, rank, ' '.join(flag)))
    if flag: bad.append(e['key'])

cl = statistics.mean(len(e['correct']) for e in data)
dl = statistics.mean(len(d) for e in data for d in e['distractors'])
strict_longest = sum(1 for e in data
    if len(e['correct']) > max(len(d) for d in e['distractors']))
print('\nmean correct %.1f  mean distractor %.1f' % (cl, dl))
print('strictly longest correct: %d/%d (%.0f%%)' % (strict_longest, len(data), 100*strict_longest/len(data)))
print('rank distribution:', {r: ranks.count(r) for r in (1,2,3,4)})
print('flagged:', bad)

json.dump(data, open('/tmp/fixed_5.json','w'), ensure_ascii=False, indent=1)
print('written', len(data), 'entries to /tmp/fixed_5.json')
