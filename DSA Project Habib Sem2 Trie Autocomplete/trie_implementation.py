from pprint import *
import json

#Create and return a new trie node for branching
def create_node():
    return {
        'child': {},
        'last': False
        }


#Insert a word into the trie and serialize the trie
def insert_word(root, key, filename='new_trie.json'):
    
    #Start from root
    node = root
    
    #Iterate through each char in key
    for char in key:
        
        #If char is not child of node, then add new branch
        if char not in node['child']:
            node['child'][char] = create_node()
        
        #Or else Move down the tree
        node = node['child'][char]
    
    #Update value of last to True, to indicate end of word
    node['last'] = True
    
    
    # Serialize the updated trie into json file
    serialize(root, filename)


#Remove a word from the trie and serialize the trie
def remove_word(root, word, filename):
    
    #Check if file exists in PC
    try:
        
        #Start finding word from root
        node = root
        list = []
        
        #Check if word even exists in trie
        for char in word:
            if char not in node['child']:
                print(f'Error: {word} does not exist.')
                return
            list.append((node, char))
            node = node['child'][char]

        #Setting 'last' to False and removing nodes if they are not needed
        node['last'] = False

        #Iterating each word's specific location in dict
        for parent, char in reversed(list):

            #Remove char from parent node completely
            if not node['child'] and not node['last']:
                parent['child'].pop(char, None)

            #Go up from leaf node to root node 
            node = parent
        
        # Serialize the updated trie into json file
        serialize(root, filename)
        
    except FileNotFoundError:
        print("Error: File not found")

    # Serialize the updated trie
    serialize(root, filename)


"""Helper function to recursively find suggestions starting from a given prefix"""
def suggestions_finder(node, prefix, suggestions):
    
    #Base Case: Starts backtracking when last is True
    if node['last']:
        suggestions.append(prefix)

    #Branches off to all children with the prefix char
    for char, child_node in node['child'].items():
        suggestions_finder(child_node, prefix + char, suggestions)


"""Find words with a given prefix in the trie."""
def print_auto_suggestions(root, prefix):
    
    #Start from root
    node = root
    
    #Check if prefix exists in trie
    for char in prefix:
        
        if char not in node['child']:
            return [] 
        node = node['child'][char]
    
    #Recursively find suggestions from prefix
    suggestions = []
    suggestions_finder(node, prefix, suggestions)
    return suggestions



"""Save the Trie as a json file"""
def serialize(trie, filename='new_trie.json'):
    with open(filename, "w") as f:
        
        #Store the updated trie as dictionary in a dynamic json file
        json.dump(trie, f, indent=4)
        

"""Loads the Trie from a JSON file."""
def deserialize(filename='new_trie.json'):
    
    #Check if the file exists
    try:
        #return trie from json file
        with open(filename, "r") as f:
            return json.load(f)

    
    except FileNotFoundError:
        print("Error: File not found")
        
        #Return a new trie as a start
        return create_node()

# def move_to_top(root, word):
#     pass



    
#Data sets
urdu_words = [
    "کتاب", "درخت", "پھول", "دریا", "سمندر", "اسکول", "بچہ", "لڑکی", "لڑکا", "سڑک", 
    "چمچ", "پانی", "ہوا", "مٹی", "آسمان", "زمین", "چاند", "سورج", "ستارہ", "جنگل", 
    "دروازہ", "گلاب", "خوراک", "پتلون", "عید", "خوشبو", "خوشی", "درد", "محبت", "فطرت", 
    "زندگی", "محنت", "کامیابی", "ہوش", "دماغ", "پہاڑ", "جزیرہ", "وطن", "دوست", "دشمن", 
    "کھیل", "جنگ", "صلح", "آزادی", "علم", "حکمت", "شعر", "پنجابی", "پشتو", "بلوچی", 
    "کہانی", "گانا", "فلم", "خبر", "چین", "آرام", "بات", "گہرا", "نیا", "پرانا", "نرم", 
    "سخت", "آلودہ", "صاف", "اجنبی", "اپنے", "دوسرا", "دنیا", "ہاتھ", "پاؤں", "ناک", "آنکھ", 
    "کان", "منہ", "زبان", "دھیما", "تیز", "خاموش", "شور", "عجیب", "خوبصورت", "بدصورت", "سچ", 
    "جھوٹ", "اچھا", "برا", "کم", "زیادہ", "شور", "سکون", "ماں", "والد", "بھائی", "بہن", "بیٹا", 
    "بیٹی", "خاندانی", "گاؤں", "شہر", "مکان", "دروازہ", "کھڑکی", "کمبل", "تکیہ", "کمرہ", 
    "فریزر", "کتاب", "کاپی", "قلم", "دفتر", "سیکنڈ", "منٹ", "گھنٹہ", "دن", "ہفتہ", "مہینہ", 
    "سال", "تاریخ", "وقت", "موسم", "سردی", "گرمی", "بارش", "برف", "ہوا", "آندھی", "طوفان", 
    "دھوپ", "چمک", "بادل", "رنگ", "سفید", "کالا", "سبز", "پیلا", "نیلا", "سرخ", "رنگین", 
    "پچاس", "سو", "ہزار", "لاکھ", "کروڑ", "ارب", "منصوبہ", "کمپنی", "تنظیم", "ادارہ", "سکول", 
    "یونیورسٹی", "کالج", "تعلیم", "استاد", "شاگرد", "مطالعہ", "سیکھنا", "سمجھنا", "لکھنا", "پڑھنا", 
    "بولنا", "سننا", "دیکھنا", "ٹرین", "بس", "گاڑی", "موٹر سائیکل", "ہوائی جہاز", "کشتی", "ریلوے", 
    "اسٹیشن", "ایئرپورٹ", "اسکول", "کھیل", "دوڑ", "کرکٹ", "فٹ بال", "والی بال", "ٹینس", "بیڈمنٹن", 
    "سکواش", "کبڈی", "کشتی", "چمچ", "گلاس", "چمچم", "کٹورا", "پلیٹ", "گھریلو", "آلہ", "برتن", 
    "کار", "چمچ", "کپڑا", "کیمرا", "ریڈیو", "ٹیلی ویژن", "ایل ای ڈی", "کمپیوٹر", "موبائل", "فون", 
    "انٹرنیٹ", "ویب", "ای میل", "سوشل میڈیا", "بلاگ", "پیغام", "ٹیکس", "قرض", "تجارت", "کاروبار", 
    "مارکیٹ", "کمیشن", "منافع", "نقصان", "سرمایہ کاری", "منظم", "فنی", "کام", "خدمت", "ضرورت", 
    "شادی", "سفر", "دعا", "خیریت", "موارد", "آرائش", "سیاست", "مقدس", "مجاز", "عید", "غصہ", 
    "خوف", "یاد", "مذہب", "خوشی", "غم", "طاقت", "فیصلہ", "رنگین", "حسین", "سوچ", "ادھورے", 
    "دور", "منزل", "موٹیویشن", "سیاسی", "معاشی", "رہنمائی", "ترقی", "نمائش", "خاندان", "تصویر", 
    "سیل", "شور", "خصوصی", "ترتیب", "بازار", "سندھ", "بلوچستان", "پنجاب", "کے پی کے", "اسلام آباد", 
    "مکتبہ", "محفل", "خاندان", "دھیما", "پراگندہ", "کیفیت", "ملاقات", "یادگار", "نتیجہ", "بصیرت", 
    "نظریہ", "مقصد", "پروگرام", "کامیابی", "تقدیر", "اللہ", "معاف", "حلال", "حرام", "رشتہ", 
    "وقت", "ایجنڈا", "خوف", "ہمت", "سچ", "جھوٹ", "گفتگو", "غصہ", "سکون", "دوستی", "دشمنی", 
    "روٹی", "کھانا", "پانی", "گوشت", "دال", "سبزی", "چاول", "نہاری", "قورمہ", "دہی", 
    "چائے", "کافی", "مٹھائی", "پھل", "موز", "سیب", "انگور", "کیلا", "آم", "پانی", 
    "کاسٹر", "پرندہ", "جانور", "گائے", "گھوڑا", "کتا", "بلی", "ہاتھی", "خرگوش", "خچچر", 
    "گلاب", "چمچ", "شادی", "زفاف", "خوشبو", "تھکاوٹ", "دکھ", "سکون", "دیکھنا", "محنت", 
    "تجربہ", "محبت", "صحت", "گھر", "کمرہ", "چمچم", "اچھی", "کامیاب", "دیکھنا", "بازی", 
    "سست", "دھیما", "زیادہ", "بہت", "کتنا", "کتنی", "کیا", "کون", "کیا", "کیسے", "کیوں", 
    "تو", "یہ", "وہ", "ہم", "وہ", "میرے", "تمہارے", "وہ لوگ", "یہ لوگ", "کل", "آج", 
    "کل", "وقت", "سال", "دن", "مہینہ", "گھنٹہ", "منٹ", "سکون", "طاقت", "جدوجہد", 
    "تعلیم", "علم", "ہمت", "اسکول", "شادی", "حالات", "خاندانی", "سیلاب", "گزرنا", 
    "مشکل", "شور", "موزی", "سمجھنا", "پھیلا", "موقع", "تجربہ", "فراہم", "مدد", 
    "پھر", "واپس", "پہنچنا", "خبر", "انتظار", "خالی", "گھرا", "کتنا", "ساگر", "سمندر"
]

english_words = ["during", "together", "across", "table", "head", "finish", "better", "before", "support", "more", 
    "much", "these", "guy", "work", "team", "fact", "side", "back", "far", "try", "each", 
    "little", "name", "off", "across", "ask", "since", "done", "stay", "different", "keep", 
    "move", "call", "ready", "lot", "school", "world", "each", "general", "answer", "service", 
    "place", "reason", "do", "event", "again", "bring", "important", "well", "ready", "call", 
    "everyone", "perhaps", "possible", "value", "find", "location", "big", "moment", "home", 
    "believe", "quick", "useful", "change", "stay", "true", "open", "rely", "last", "fine", 
    "nice", "find", "chance", "connect", "service", "people", "continue", "meeting", "figure", 
    "work", "better", "use", "further", "lead", "really", "finish", "direct", "provide", "common", 
    "ask", "difficult", "approach", "lot", "market", "take", "family", "information", "travel", 
    "rate", "begin", "start", "helpful", "hard", "show", "success", "field", "self", "personal", 
    "today", "grow", "necessary", "prove", "reason", "strong", "open", "call", "plan", 
    "continue", "continue", "important", "end", "difficult", "sign", "level", "understand", 
    "affect", "use", "place", "back", "run", "find", "lot", "attempt", "work", "response", 
    "feeling", "plan", "progress", "most", "team", "assistance", "message", "home", "go", 
    "provide", "position", "ask", "way", "second", "extra", "help", "meet", "please", "keep", 
    "focus", "true", "better", "rely", "provide", "change", "team", "lot", "best", "problem", 
    "care", "situation", "even", "risk", "speak", "position", "extra", "more", "move", 
    "kind", "positive", "line", "care", "require", "increase", "question", "attempt", "start", 
    "school", "future", "plan", "helpful", "guess", "team", "project", "return", "question", 
    "today", "day", "remember", "hold", "difference", "continue", "start", "office", "system", 
    "outside", "suggest", "reason", "area", "improve", "try", "life", "decision", "environment", 
    "factor", "feel", "big", "opportunity", "here", "situation", "company", "change", 
    "open", "suggestion", "kind", "situation", "report", "process", "direction", "small", 
    "activity", "turn", "return", "new", "speak", "work", "next", "point", "find", 
    "stay", "situation", "share", "speak", "change", "relate", "talk", "long", "work", 
    "fall", "price", "nothing", "goal", "case", "help", "start", "pick", "sure", 
    "current", "balance", "type", "compare", "understand", "move", "different", "change", 
    "act", "involve", "future", "level", "significant", "plan", "control", "space", 
    "turn", "wait", "please", "talk", "success", "maintain", "feel", "through", 
    "leave", "limit", "thank", "provide", "answer", "offer", "end", "return", 
    "lead", "care", "more", "turn", "decision", "every", "complete", "go", "reason", 
    "within", "plan", "find", "finish", "result", "ask", "person", "suggest", 
    "place", "difficult", "point", "place", "future", "measure", "research", "option", 
    "finally", "arrive", "great", "result", "put", "feel", "believe", "chance", 
    "care", "increase", "through", "effect", "allow", "common", "create", "might", 
    "feeling", "plan", "team", "show", "long", "realize", "make", "find", 
    "again", "last", "line", "cause", "suggest", "stay", "yet", "great", 
    "run", "check", "leave", "clear", "change", "purpose", "home", "understand", 
    "point", "matter", "sort", "process", "clear", "week", "family", "join", 
    "process", "again", "near", "work", "approach", "team", "fact", "move", 
    "stay", "group", "first", "complete", "due", "begin", "situation", "thought", 
    "decision", "match", "through", "plan", "start", "ready", "address", 
    "support", "decision", "ask", "part", "target", "relate", "matter", 
    "company", "finish", "opportunity", "situation", "check", "start", "support", 
    "will", "after", "plan", "open", "list", "general", "pay", "offer", 
    "response", "success", "provide", "expect", "check", "interest", "new", 
    "place", "test", "possible", "group", "might", "mention", "close", 
    "free", "make", "best", "live", "current", "place", "quick", "family", 
    "able", "support", "help", "job", "school", "family", "case", "help", 
    "plan", "possible", "gather", "new", "fast", "love", "connect", "goal", 
    "group", "hard", "try", "easy", "choose", "today", "move", "down", 
    "different", "feeling", "end", "process", "set", "call", "line", 
    "care", "now", "ready", "find", "class", "meeting", "soon", "way", 
    "whole", "finally", "reply", "reason", "large", "situation", "same", 
    "take", "end", "clear", "put", "realize", "person", "through", 
    "method", "solution", "meeting", "plan", "choose", "read", "move", 
    "result", "true", "result", "manage", "find", "begin", "wish", 
    "back", "consider", "show", "feel", "information", "plan", "question", 
    "ask", "year", "guess", "plan", "use", "now", "sure", "reply", 
    "bring", "finish", "option", "hard", "matter", "term", "key", 
    "end", "clear", "hold", "help", "suggest", "choose", "approach", 
    "life", "finish", "ask", "time", "period", "question", "sign", 
    "use", "try", "matter", "choose", "send", "match", "really", 
    "stop", "look", "condition", "change", "feel", "end", "plan", 
    "head", "team", "answer", "strong", "go", "move", "cause", 
    "return", "show", "help", "question", "group", "choose", "life", 
    "hope", "sign", "meet", "plan", "suggest", "relate", "work", 
    "start", "speak", "understand", "test", "plan", "significant", 
    "choose", "stay", "end", "help", "situation", "meet", "condition",
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", 
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", 
    "this", "but", "his", "by", "from", "they", "we", "say", "her", 
    "she", "or", "an", "will", "my", "one", "all", "would", "there", 
    "their", "what", "so", "up", "out", "if", "about", "who", "get", 
    "which", "go", "me", "when", "make", "can", "like", "time", 
    "no", "just", "him", "know", "take", "people", "into", "year", 
    "your", "good", "some", "could", "them", "see", "other", "than", 
    "then", "now", "look", "only", "come", "its", "over", "think", 
    "also", "back", "after", "use", "two", "how", "our", "work", 
    "first", "well", "way", "even", "new", "want", "because", "any", 
    "these", "give", "day", "most", "us", "is", "are", "was", "were", 
    "am", "become", "through", "life", "too", "too", "those", "tell", 
    "very", "good", "people", "find", "long", "down", "day", "need", 
    "tell", "mean", "call", "great", "how", "big", "small", "find", 
    "go", "put", "set", "must", "right", "end", "call", "show", 
    "because", "understand", "point", "off", "home", "help", 
    "around", "live", "before", "take", "move", "live", "get", 
    "love", "problem", "should", "try", "use", "care", "possible", 
    "reason", "feel", "believe", "hurt", "might", "big", "place", 
    "state", "head", "picture", "group", "work", "world", "want", 
    "health", "best", "change", "begin", "question", "tell", 
    "figure", "answer", "point", "continue", "must", "information", 
    "left", "ready", "make", "system", "receive", "try", "certain", 
    "everything", "real", "right", "bit", "type", "seem", "separate", 
    "read", "look", "sometimes", "start", "real", "few", "move", 
    "past", "meet", "certain", "true", "keep", "different", "clear", 
    "leave", "matter", "situation", "problem", "sound", "up", "old", 
    "life", "reason", "outside", "stop", "such", "under", "away", 
    "problem", "key", "definitely", "search", "do", "say", "solution", 
    "now", "question", "talk", "yet", "consider", "next", "live", 
    "remain", "example", "change", "own", "again", "plan", "wrong", 
    "speak", "hear", "call", "environment", "wish", "present", 
    "suggest", "go", "work", "idea", "sometimes", "right", "around", 
    "apply", "different", "understand", "experience", "buy", 
    "run", "top", "sure", "happen", "know", "improve", "same", 
    "spend", "need", "because", "value", "money", "important", 
    "whether", "come", "find", "support", "part", "expect", 
    "speak", "pick", "hard", "balance", "expected", "outside", 
    "let", "wait", "friend", "take", "group", "week", "problem", 
    "change", "relationship", "set", "finish", "quality", "after", 
    "work", "book", "use", "answer", "might", "too", "second", 
    "big", "sometimes", "ask", "complete", "suggest", "friend", 
    "question", "best", "moment", "activity", "keep", "experience", 
    "effort", "know", "give", "would", "often", "process", "work", 
    "problem", "mention", "point", "set", "fact", "week", "focus", 
    "stay", "improve", "really", "talk", "become", "help", "share", 
    "feel", "enough", "go", "believe", "carry", "travel", "about", 
    "service", "place", "nearly", "much", "together", "research", 
    "finish", "meet", "choice", "learn", "suggest", "change", 
    "work", "name", "continue", "call", "ready", "case", 
    "lead", "situation", "time", "information", "create", "learn", 
    "continue", "hope", "around", "find", "problem", "solution", 
    "fact", "simple", "plan", "organization", "target", "different", 
    "success", "share", "gather", "fun", "enjoy", "speak", "problems", 
    "efficient", "express", "mention", "completely", "hope", 
    "understand", "happy", "attempt", "group", "significant", 
    "idea", "work", "simply", "normal", "search", "information", 
    "talk", "feel", "stay", "please", "problem", "free", "through", 
    "give", "go", "specific", "wish", "type", "list", "important", 
    "realize", "final", "create", "comment", "health", "consider", 
    "long", "time", "someone", "week", "long", "plan", "condition", 
    "account", "degree", "focus", "show", "feeling", "big", 
    "again", "experience", "solution", "world", "together", 
    "start", "create", "work", "effort", "personal", "correct", 
    "maintain", "idea", "space", "worry", "front", "question", 
    "quickly", "attention", "speak", "positive", "relate", "others", 
    "thank", "finish", "result", "group", "still", "term", "instead"
    ]


def load_words_into_trie(filename="words.txt", trie_file="max_english_trie.json"):
    """Load words from file and insert into trie."""
    try:
        # Initialize or load existing trie
        trie_root = create_node()
        words = []
        # Read words from file
        with open(filename, 'r') as f:
            print("x",end='')
            for line in f:
                line = line.strip().lower()
                if line not in words:
                    words.append(line)
                    
        # Insert words into trie
        for word in words:
            insert_word(trie_root, word)
        
        # Save the trie
        serialize(trie_root, trie_file)
        
        print(f"Successfully loaded {len(words)} words into trie")
        return trie_root
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
