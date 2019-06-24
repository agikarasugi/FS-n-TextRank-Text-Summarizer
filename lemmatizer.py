import re
import mysql.connector
from nltk import word_tokenize
import pcre
from collections import OrderedDict

counter = 0

class Lemmatizer():
    
    def __init__(self):
        self.vowel = "[aiueo]"
        self.consonant = "[bcdfghjklmnpqrstvwxyz]"
        self.alpha = "[a-z]+-?[a-z]*"
        self.removed = {'particle':"",
                    'possessive_pronoun': "",
                    'derivational_suffix': "",
                    'derivational_prefix': ""
        }
        self.found = ""
        self.complex_prefix_tracker = {}
        self.recoding_tracker = {}
        self.error = ""
        self.total_lookup = 0
        self.database = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='@touF3?dip',
            database='lemmatizer'
        )
        self.time = None

    
    def lemmatize(self,word):
        self.__init__()
        ret =  self.eat(word)

        if type(ret) == tuple:
            return ret[0]
        else:
            return ret


    def lookup(self,word):

        if len(word) < 3: return False
        
        check = word
        check2 = ''
        query_string = ''

        match = pcre.search("^([a-z]+)-([a-z]+)$", check) #check repeating words like main-main
        if match:
            if match.group(1) == match.group(2):
                check = match.group(1)
                check2 = word

        
        if len(word) <= 6:
            query_string = "'{}'".format(check)
        else:
            syllabel = "([bcdfghjklmnpqrstvwxyz]|sy)?([aiueo])(?U)([bcdfghjklmnpqrstvwxyz]|ng)?"
            reg = "^(?<first>aneka|({}{}))(?<second>{}{}(?U)({})*)$".format(syllabel, syllabel, syllabel, syllabel, syllabel) #notsure if true

            match = pcre.search(reg, word)

            if match:
                query_string = "'" + match.group('first')+ ' ' +match.group('second') + "' OR lemma LIKE '{}'".format(check)
            else:
                query_string = "'{}'".format(check)
        

        if check2 != '':
            query_string += " OR lemma LIKE '{}'".format(check2)


        if pcre.search('[aiueo]$', word) and self.removed['derivational_suffix'] == 'kan' and len(word) > 3:
            query_string += " OR lemma LIKE '{}k' ORDER BY pos DESC".format(check)
        

        query = self.database.cursor()
        txt = "SELECT * FROM dictionary WHERE lemma LIKE {} LIMIT 1".format(query_string)

        try:
            query.execute(txt)
        except:
            print('error happened')

        self.total_lookup +=1

        try:
            row = query.fetchall()
        except:
            row = ""
            print('empty data')

        if row:
            self.found = row[0]

            return self.found


    def check_rule_precedence(self, word):
        # alpha = self.alpha

        patterns = [
            "^be(?<word>{})([^k]an|lah|kah)$".format(self.alpha),
            "^(me|di|pe|te)(?<word>{})(i)$".format(self.alpha),
            "^(k|s)e(?<word>{})(i|kan)$".format(self.alpha),
            "^([pm]e[nm]|di[tmp])(?<word>ah|ak|er|el)an$"
        ]

        for pattern in patterns:
            match = pcre.search(pattern, word)

            if match and match.group('word') != 'ngalam':
                return True
            
        return False

    
    def has_disallowed_pairs(self):
        # alpha = self.alpha

        patterns = [
            "^be[^r]i$",
            "^(k|s)e(i|kan)$",
            "^(di|me|te)[^krwylp]an$"
        ]

        if self.removed['derivational_prefix'] != '' and self.removed['derivational_suffix'] != '':
            prefix = self.removed['derivational_prefix'][0]

            for pattern in patterns:
                #self.removed['derivational_suffix'] = pcre.search(pattern, prefix)

                if pcre.search(pattern, prefix):
                    self.removed['derivational_suffix'] = pcre.search(pattern, prefix)
                    return True
        
        return False



    def delete_inflectional_suffix(self,word):
        result = word
        patterns = {
            'particle':"([klt]ah|pun)$",
            'possessive_pronoun':"([km]u|nya)$"
        }

        for key,pattern in patterns.items():
            match = pcre.search(pattern, result)

            if match:
                result = pcre.sub(pattern, '', result)
                self.removed[key] = match.group(0)
                check = self.lookup(result)

                if check:
                    return check
        
        return result

    def delete_derivational_suffix(self, word):
        result = word
        derivational_suffix = "(i|k?an)$"
        match = pcre.search(derivational_suffix, result)

        if match:
            result = pcre.sub(derivational_suffix, '', result)
            self.removed['derivational_suffix'] = match.group(0)
            check = self.lookup(result)

            if check:
                return check
        
        return result


    
    def delete_derivational_prefix(self,word):
        vowel = self.vowel
        consonant = self.consonant
        alpha = self.alpha
        result = word
        prefix_type = ""
        prefix = ""

        patterns = {
            'plain':"^(di|(k|s)e)",
            'complex':"^(b|m|p|t)e"
        }

        if len(result) < 4:
            return result
        
        for key,pattern in patterns.items():
            match = re.match(pattern, result)

            if match:
                prefix_type = (key == 'plain')
                prefix = match[0]
        
                if self.removed['derivational_prefix'] != '' and prefix in self.removed['derivational_prefix']:
                    return result
                
                self.recoding_tracker[match[0]] = ''

                if prefix_type:
                    array = self.removed['derivational_prefix']


                    if prefix == 'ke' and array != '' and (array[0] == 'di' and not(pcre.search('(tawa|tahu)', result)) and array[0] != 'be'):
                        return result
                    
                    result = pcre.sub(pattern, '', result)

                    self.complex_prefix_tracker[prefix] = {prefix:''}
                
                else:
                    modification = ""

                    #  'be-' prefix rules
                    #   total rule = 5

                    if prefix == 'be':

                        if self.removed['derivational_prefix'] != '':

                            array_key = list(self.complex_prefix_tracker.keys())[0] #get first dict value
                            array = self.complex_prefix_tracker[array_key]

                            added_key = list(array.keys())[0]
                            added = array[added_key]
                            pp =  added_key

                            if pp not in ['mem', 'pem', 'di', 'ke']:
                                return result
                        

                        #rule 1
                        
                        if pcre.search("^ber{}".format(vowel), result):

                            result = pcre.sub("^ber", '', result)
                            modification = {"ber":''}
                            self.recoding_tracker[prefix] = {'be':''}
                        
                        #rule 2
                        elif pcre.search("^ber[bcdfghjklmnpqstvwxyz][a-z](?!er)", result):

                            result = pcre.sub("^ber", '', result)
                            modification = {'ber':""}
                        
                        #rule 3
                        elif pcre.search("^ber[bcdfghjklmnpqstvwxyz][a-z]er{}".format(vowel), result):

                            result = pcre.sub("^ber", '', result)
                            modification = {'ber':""}

                        #rule 4
                        elif pcre.search("^belajar$", result):

                            result = pcre.sub("^bel", '', result)
                            modification = {'bel':""}

                        #rule 5
                        elif pcre.search("^be[bcdfghjkmnpqstvwxyz]er{}".format(consonant), result):

                            result = pcre.sub("^be", '', result)
                            modification = {'be':""}

                        #unsuccessful
                        else:
                            del self.recoding_tracker[prefix]
                            return word

                     # te- prefix rules
                     # total rule : 5
                        
                    elif prefix == 'te':
                        

                        if self.removed['derivational_prefix'] != '':
                            array_key = list(self.complex_prefix_tracker.keys())[0] #get first dict value
                            array = self.complex_prefix_tracker[array_key]

                            added_key = list(array.keys())[0]
                            added = array[added_key]
                            pp =  added_key

                            if pp != 'ke' and pp in ['me', 'men', 'pen'] and not(pcre.search('tawa', result)):
                                return result
                        
                        #rule 6
                        if pcre.search("^ter{}".format(vowel), result):

                            result = pcre.sub('^ter', '', result)
                            modification = {'ter':''}
                            self.recoding_tracker[prefix] = {'te':''}
                        
                        #rule 7
                        
                        elif pcre.search("^ter[bcdfghjklmnpqstvwxyz]er{}".format(vowel), result):

                            result = pcre.sub('^ter', '', result)
                            modification = {'ter':''}
                        
                        #rule 8
                        elif pcre.search("^ter{}(?!er)".format(consonant), result):

                            result = pcre.sub('^ter', '', result)
                            modification = {'ter':''}                        

                        #rule 9
                        elif pcre.search("^te[bcdfghjklmnpqstvwxyz]er{}".format(consonant), result):

                            result = pcre.sub('^te', '', result)
                            modification = {'te':''} 

                        #rule 10
                        elif pcre.search("^ter[bcdfghjklmnpqstvwxyz]er{}".format(consonant), result):

                            result = pcre.sub('^ter', '', result)
                            modification = {'ter':''}

                        #unsuccessful
                        
                        else:
                            del self.recoding_tracker[prefix]
                            return word                                         

                    # me- prefix rules
                    # total rule = 10

                    elif prefix == 'me':
                        
                        
                        if self.removed['derivational_prefix'] != '':
                            return result
                        
                        #rule 11
                        if pcre.search('^me[lrwy]{}'.format(vowel), result):

                            result = pcre.sub('^me', '', result)
                            modification = {'me':''}
                        
                        #rule 12
                        
                        elif pcre.search('^mem[bfv]', result):

                            result = pcre.sub('^mem', '', result)
                            modification = {'mem':''}
                        
                        #rule 13
                        elif pcre.search('^mempe', result):

                            result = pcre.sub('^mem', '', result)
                            modification = {'mem':''}

                        #rule 14
                        elif pcre.search("^mem(r?)[aiueo]", result):
                            match = pcre.search("^mem(r?)[aiueo]", result)
                            result = pcre.sub('^me', '', result)
                            modification = {'me{}'.format(match.group(1)):''}
                            self.recoding_tracker[prefix] = {'mem':'p'}

                        #rule 15
                        
                        elif pcre.search('^men[cdsjz]', result):

                            result = pcre.sub('^men', '', result)
                            modification = {'men':''}

                        #rule 16
                                                                      
                        elif pcre.search('^men{}'.format(vowel), result):

                            result = pcre.sub('^men', 't', result)
                            modification = {'men':'t'}
                            self.recoding_tracker[prefix] = {'me':''}

                        #rule 17
                        
                        elif pcre.search('^meng[ghqk]', result):

                            result = pcre.sub('^meng', '', result)
                            modification = {'meng':''}

                        #rule 18
                        
                        elif pcre.search('^meng({})'.format(vowel), result):
                            match = pcre.search('^meng({})'.format(vowel), result)
                            result = pcre.sub('^meng', '', result)
                            modification = {'meng':''}

                            self.recoding_tracker[prefix] = {'meng1':'k'}
                            self.recoding_tracker[prefix]['menge'] = ''
                        
                        #rule 19
                        elif pcre.search('^meny{}'.format(vowel), result):

                            result = pcre.sub('^me', '', result)
                            modification = {'me':''}
                            self.recoding_tracker[prefix] = {'meny':'s'}
                        
                        #rule 20
                        elif pcre.search('^memp[abcdfghijklmnopqrstuvwxyz]', result):

                            result = pcre.sub('^mem', '', result)
                            modification = {'mem':''}
                        
                        #unsuccesful
                        else :
                            del self.recoding_tracker[prefix]
                            return word
                        
                    
                    # pe- prefix rules
                    # total rule = 15

                    elif prefix == 'pe':

                        if self.removed['derivational_prefix'] != '':
                            array_key = list(self.complex_prefix_tracker.keys())[0] #get first dict value
                            array = self.complex_prefix_tracker[array_key]

                            added_key = list(array.keys())[0]
                            added = array[added_key]
                            pp =  added_key

                            if  pp not in ['di', 'ber', 'mem', 'se', 'ke']:
                                return result
                        
                        #rule 21
                        if pcre.search('^pe[wy]{}'.format(vowel), result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''}                        

                        #rule 22
                        elif pcre.search('^per{}'.format(vowel), result):

                            result = pcre.sub('^per', '', result)
                            modification = {'per':''} 
                            self.recoding_tracker[prefix] = {'pe':''}
                        
                        #rule 23
                        elif pcre.search('^per[bcdfghjklmnpqstvwxyz][a-z](?!er)', result):

                            result = pcre.sub('^per', '', result)
                            modification = {'per':''}                         

                        #rule 24
                        elif pcre.search('^per[bcdfghjklmnpqstvwxyz][a-z]er{}'.format(vowel), result):

                            result = pcre.sub('^per', '', result)
                            modification = {'per':''}
                        
                        #rule 25
                        elif pcre.search('^pem[bfv]', result):

                            result = pcre.sub('^pem', '', result)
                            modification = {'pem':''}
                        
                        #rule 26
                        elif pcre.search('^pem(r?){}'.format(vowel), result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''} 
                            self.recoding_tracker[prefix] = {'pem':'p'}                       

                        #rule 27
                        elif pcre.search('^pen[cdjz]', result):

                            result = pcre.sub('^pen', '', result)
                            modification = {'pen':''}

                        #rule 28
                        elif pcre.search('^pen{}'.format(vowel), result):

                            result = pcre.sub('^pen', 't', result)
                            modification = {'pen':'t'} 
                            self.recoding_tracker[prefix] = {'pe':''}

                        #rule 29
                        elif pcre.search('^peng{}'.format(consonant), result):

                            result = pcre.sub('^peng', '', result)
                            modification = {'peng':''}

                        #rule 30
                        elif pcre.search('^peng({})'.format(vowel), result):
                            match = pcre.search('^peng({})'.format(vowel), result)
                            result = pcre.sub('^peng', '', result)
                            modification = {'peng':''}

                            self.recoding_tracker[prefix] = {'peng1':'k'}
                            self.recoding_tracker[prefix]['penge'] = ''

                        #rule 31
                        elif pcre.search('^peny{}'.format(vowel), result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''} 
                            self.recoding_tracker[prefix] = {'peny':'s'}
                        
                        #rule 32
                        elif pcre.search('^pel{}'.format(vowel), result):
                            
                            if (result == 'pelajar'):
                                result = pcre.sub('^pel', '', result)
                                modification = {'pel':''}
                            else:
                                result = pcre.sub("^pe", "", result)
                                modification = {'pe':''}
                        
                        #rule 33
                        elif pcre.search('^pe[bcdfghjkpqstvxz]er{}'.format(vowel), result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''}
                        
                        #rule 34
                        elif pcre.search('^pe[bcdfghjkpqstvxz](?!er)', result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''} 

                        #rule 35
                        elif pcre.search('^pe[bcdfghjkpqstvxz]er{}'.format(consonant), result):

                            result = pcre.sub('^pe', '', result)
                            modification = {'pe':''}

                        #unsuccessful
                        else:
                            del self.recoding_tracker[prefix]
                            return word

                    if modification != "":
                        self.complex_prefix_tracker[prefix] = modification
                    else:
                        return result


                if self.removed['derivational_prefix'] == '':
                    self.removed['derivational_prefix'] = []
                
                self.removed['derivational_prefix'].append(prefix)
                self.lookup(result)
                return result
                                                 
        return result

    def recode(self, word):
        result = word
        prefixes = self.complex_prefix_tracker 
        reverse_ord = list(prefixes.keys())
        reverse_ord.reverse()
    


        for prefix,changes in prefixes.items():
            recode = self.recoding_tracker[prefix]
            prefix_key = list(changes.keys())[0] 
            prefix_added = changes[prefix_key]
            prefix_removed = prefix_key
            temp = ""

            #the code below is different from the original code due to how python insert values to dict
            if prefix_added != '':
                result = pcre.sub('^{}'.format(prefix_added), prefix_removed, result)
            else:
                result = prefix_removed + result
            
            if recode != '':
                temp = ""
                temp2 = ""

                for raw_removed, added in recode.items():
                    removed = pcre.sub("[0-9]+", "", raw_removed)
                    if added:
                        temp2 = added
                    else:
                        temp2 = ""

                    temp = pcre.sub('^{}'.format(removed), temp2, result)

                    if self.lookup(temp):
                        self.complex_prefix_tracker[prefix] = {removed:added}
                        return temp
                    
                    previous = ''
                    record = temp
                    before = len(self.complex_prefix_tracker)

                    for i in range(3):
                        previous = record

                        record = self.delete_derivational_prefix(record)

                        if (i == 0 and self.has_disallowed_pairs()) or record == previous or len(self.removed['derivational_prefix']) > 3:
                            break
                        elif self.found:
                            return record

                    if len(self.complex_prefix_tracker) > before:
                        tempe = dict(self.complex_prefix_tracker)
                        count = 0
                        for key,value in tempe.items():
                            count +=1
                            if count <= before:
                                continue
                            
                            del self.complex_prefix_tracker[key]
                            del self.removed['derivational_prefix'][count-1]

            #disabling this for now 
            # if temp != "":
            #     result = temp
            
        return word
        
    def eat (self, word, backtrack_step = False):
        result = word
        temp = self.lookup(word)

        if temp:
            if not(backtrack_step):
                self.error = 'input_is_lemma'
                return temp
        else:
            steps = self.check_rule_precedence(word)

            if(backtrack_step):
                steps = [5,6]
            else:
                if (steps):
                    steps = [5,6,3,4,7]
                else:
                    steps = [3,4,5,6,7]
            
        for step in steps:
            if step == 3: 
                temp = self.delete_inflectional_suffix(result)
                

            elif step == 4:
                temp = self.delete_derivational_suffix(result)
                

            elif step == 5:
                temp = result

                for i in range (3):
                    previous = temp
                    temp = self.delete_derivational_prefix(temp)

                    if ( (i == 0 and self.has_disallowed_pairs()) or self.found or temp == previous or (type(self.removed['derivational_prefix']) is str and len(self.removed['derivational_prefix'] > 3))):
                        break
                
            
            elif step == 6:
                temp = self.recode(result)
                
            
            elif step == 7:
                prefixes = self.complex_prefix_tracker 
                res = temp
                temp = ""
                

                for prefix, changes in prefixes.items():
                    changes_first_key = list(changes.keys())[0]

                    prefix_added = changes[changes_first_key]
                    prefix_removed = changes_first_key
                
                    if prefix_added != '':
                        temp = pcre.sub('^{}'.format(prefix_added), prefix_removed, temp)

                    else:
                        temp = temp + prefix_removed 
                    
                
                self.removed['derivational_prefix'] = ''
                self.complex_prefix_tracker = {} 
                temp = temp + res
                backtract = self.eat(temp, True)

                if self.found:
                    return self.found

                #return deriv suffix
                if not(self.found) and self.removed['derivational_suffix'] != '':

                    if self.removed['derivational_suffix'] == 'kan':

                        temp = temp+'k'
                        self.removed['derivational_prefix'] = ''
                        self.complex_prefix_tracker = {} 
                        backtract = self.eat(temp, True)

                        if self.found:
                            return self.found
                        
                        temp = temp + 'an'
                
                    else:
                        temp = temp + self.removed['derivational_suffix']
                    
                    self.removed['derivational_prefix'] = ''
                    self.complex_prefix_tracker = {} 
                    backtract = self.eat(temp, True)

                #return possessive pronoun
                if not(self.found) and self.removed['possessive_pronoun'] != '':
                    temp = temp + self.removed['possessive_pronoun']
                    self.removed['derivational_prefix'] = ''
                    self.complex_prefix_tracker = {} 
                    backtract = self.eat(temp, True)

                    if self.found :
                        return self.found
                
                #return particle
                if not(self.found) and self.removed['particle'] != '':
                    temp = temp + self.removed['particle']
                    self.removed['derivational_prefix'] = ''
                    self.complex_prefix_tracker = {} 
                    backtract = self.eat(temp, True)

                    if self.found :
                        return self.found

            if self.found:
                return self.found

            result = temp

        if not(backtrack_step) and not(self.error):
            self.error = 'lemma_not_found'

        return word     