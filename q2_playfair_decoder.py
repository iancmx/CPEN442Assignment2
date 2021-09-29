import math
import random

# Quadgram frequency file obtained from http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
quadgram_file = "english_quadgrams.txt"

# Quadgram scoring function based on the logic described in http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
class quadgram_scoring_function:
    def __init__(self):
        with open(quadgram_file) as file:
            lines = file.readlines()
        self.quadgrams_dict = {}
        for line in lines:
            quadgram, count = line.split(' ')
            self.quadgrams_dict[quadgram] = int(count)
        self.total_quadgram_count = sum(self.quadgrams_dict.values())

        # Calculate the Log Probabilities where p(x) = count(x)/total_quadgram_count
        for quadgram in self.quadgrams_dict.keys():
            quadgram_count = self.quadgrams_dict[quadgram]
            self.quadgrams_dict[quadgram] = math.log10(float(quadgram_count)/self.total_quadgram_count)

    def score(self, text):
        score = 0
        for i in range(len(text) - 3):
            if text[i:i+4] in self.quadgrams_dict:
                score += self.quadgrams_dict.get(text[i:i+4])
            else:
                score += math.log10(0.01/self.total_quadgram_count)
        return score


def playfair_decrypt(key, ciphertext):
    plaintext = ""
    for i in range(0, len(ciphertext) - 1, 2):
        bigram = ciphertext[i:i+2]
        row_index_1 = int(key.index(bigram[0]) / 5)
        column_index_1 = key.index(bigram[0]) % 5
        row_index_2 = int(key.index(bigram[1]) / 5)
        column_index_2 = key.index(bigram[1]) % 5

        if column_index_1 == column_index_2:
            plaintext += key[((row_index_1 - 1) % 5) * 5 + column_index_1]
            plaintext += key[((row_index_2 - 1) % 5) * 5 + column_index_2]
        elif row_index_1 == row_index_2:
            plaintext += key[row_index_1 * 5 + ((column_index_1 - 1) % 5)]
            plaintext += key[row_index_2 * 5 + ((column_index_2 - 1) % 5)]
        else:
            plaintext += key[row_index_1 * 5 + column_index_2]
            plaintext += key[row_index_2 * 5 + column_index_1]

    return plaintext

def random_letter_swap(primary_key):
    temp_list = list(primary_key)
    first_letter_index = random.randrange(len(primary_key))
    second_letter_index = random.randrange(len(primary_key))
    temp_list[first_letter_index], temp_list[second_letter_index] = temp_list[second_letter_index], temp_list[first_letter_index]
    return ''.join(temp_list)

def simmulated_annealing(ciphertext):
    alphas = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    best_key = ''.join(random.sample(alphas, len(alphas)))
    fitness = quadgram_scoring_function()
    highest_score = fitness.score(playfair_decrypt(best_key, ciphertext))
    temp_best_score = highest_score
    anneal_temp = 50
    step = 0.5

    while anneal_temp >= 0:
        for num_runs in range(10000):
            modified_key = random_letter_swap(best_key)
            decrypted_text = playfair_decrypt(modified_key, ciphertext)
            score = fitness.score(decrypted_text)
            delta = score - highest_score
            if delta >= 0:
                best_key = modified_key
                temp_best_score = score
            elif anneal_temp > 0:
                probability = math.exp(delta/anneal_temp)
                if random.random() < probability:
                    best_key = modified_key
                    temp_best_score = score

            if temp_best_score > highest_score:
                highest_score = temp_best_score
                print("BEST SCORE", highest_score)
                print(best_key)
                print(decrypted_text)

        anneal_temp -= step


problem_2_encrypted_string = "KGGIKGYUYKCIVUVZGIMBWQVBKCLQCIRAGKOVKFRANDVYXEWDZYNPAWGIMHXYVLWTMRLCGIAXKIQIZLGIXZKMNPVUIKBQSIXERTGIKENHFBFTKIYKQZESYMWDMXKHIPCLCLUVCLGIKEBQOPVSKRPUFNGIKFDHWTLCGKAKYGCBHQYGNKCTUYYMLZIFRAKOZOPVBCGNKMVZCPVUPNRALCCYZLGRXELVVPKMGIXEWDZYWMSIFIRKVUCIRANDVYXECBMXQZESYMQAKTRGKIFKVDXEMWXAFBGYNDTGRAAVMHXYKXYMRMLZIDXEVUGTKCYGVBWDMFKTAKMPGDXEWYNMKFVUITUYKMVLWTQZESYMLCLCQZESYMWDMXKHRSVUGNAXVTFPCLCLRAKYXEYGIUKIEMSIMWNIRAFHKMLCQRQBLCFALNKQNICYKWWMWMHWKCVUPNRAOTUBMRGIMRZBZVQZESYMVLTNMRKIQZESYMKWMDCPGIKAKEQKEXPZFBVBKCGIMFZQAKLCGRXEVIMXUMCLKWMUZQUYYMNHGILCLCFICLIKWTYGCBPWLOXEVBXYDHSIRAIZUYYMWDMXGKIFMRCBRAIHZOIXKEVUFNGIXEAXXEMXYRXEYGVZMHBWKMVXKOUYYMSOIKPIHVBCFNGKAKRAVFCBPGZLKCIPRACBMFYHMRNHGIEKFBVLSXIHTNUMCLNHGIKCMWVQIFIKYKWDAXMWQWTYKCLWIHNMVBLCQWIVGIXZKYXEYGIUKIKOUYYMRADXVTRYDXVQMXIKCNTVWTYKEZIHVBCBGIAREHIUUYYMEKFBVLXHQYVSMRVUFNGIMXCSWDCBYXIHHAGKSIGIYXHIMUWMWTBSXZKFVBQZESYMKWRSVUVZGIMVHVBCGTXZYFXKEHVBBUWYHMBMZOKDHAFNGIKCAMTVFNGFAFHIGBZOPVQAQVMHXYKXUPRSRMBTABDHNMMRWQMEREUYRAVZSWQZCSFIEMSIXMPIQBCKCIRAKDMULCGENPHEWTYFKWRSVUPNRAQWBNUPDFIHXMIUUYYMMWWDAXYGAKHMVLWTQZESYMLCXMARQBFDKFLKGIKZZOCIVEQWWMOLCPRAIVCLGIXEAXXEKXKMGTKXZKWMFNGIMXHVMXZLGIXEQYIUUYYMGMKCFKHMHMKCLKOVZMQZVLIZUYYMKWVSKECBIPRAASXEXRRKPVBUTPHEKCKWVRAFKFYWFYNDWKSOSIKWZKVUFKRHRMCIVBGIKYCSQINKWBXAEXLQUVGEDEXEWMSIYWFYLCHEDNYFEHFAZIULUMCLCBZKKCWQDHFYWDAXZOPVGMBNWMVQPUKZUYYMKWIPRAFMULFYQKYKZOFNLCVLCYKGRAHESIOLBGQBMWWDAXKXLNELZVYRXEBLXKNCAXWDARMHXYKXGIKYKMWBZLRMNPVZKVWTGIAXKTAKHSKIQIKWMUKFIKWTGIKYREXZXRVZYSCBHMFAVUFNGIARZOXMBUTGRASPCTIAKCBSXEYZRSVPZBCYKCPHXAFBTVWTNUUYYMLZEXKQAQMWVZCSIUUYYMNHGIYWHTVUYKLZHEVZZLVUGKFBGBXEMFKHCIMROVZMQZESYMLZIHCIDHNUZOCIVEZLGIXZKMNPOVZMQWNPRAGEYLIHFKQZVLIVCLLCQWIVYRKXKCTQUYYMQAKXVUVZGIABMWIKEXHSKIRWRAVFCBHQYGAMSIXYHWCIQBCBRMHXRAEXWDMXVQOPMDMWNPRACKHAITUYYMWDKZMYKFQYVQPUXEKGRAVFEHFAIFAWCIRAEXNPVULCCIRAFHXZKXGYSWXYLZEXKIYMBKYKWKSIBQYKWSXEMRKWTKWTVUGTHRYFKIGFXRHVVPXEUDGYEKHMBPZOVPEMUDUBNDOVKZUYYMKWIPRAFMULFYXAEXGYQPDHWTKWMUKCTHWTQZESYMQAVTKMNVPGYWFYXKEHOBQWBPQYRMHSKIDVYFKTVCPURECDPNKWISCPNUUYYMTDMXKWIUMAMXQZESYMKWMSKWBLGIXELQUVGIKCPWLCKMPICLGIMFYZLFAFEXKFMRVUVZGIEAKCVPKOUYYMKWVHBIKIMRRAIFUBPDFMHESILCGMBNNPRACKHAGNKIIGRAEPZVGIDNQWNPRAVQYKZLCBYZTGRAIHQIMXPKCSQINKWBKCGIYFKWIUUYYMKWVDDNRERKSIBSXEAFKGRAEXHSKIRWDHKPZQYFYXHEFKGIKREREXMRUYREUYGIYXCBHMFAZLGIAXKTAKHSKIQIVUPIZVCLVAKGKMRAEHLKUPFSFMHESIQWBSKHFKMPLUWXKLRAIHQISPCTIAKCDHSUYFTZUYYMQAUBKXMYAXMWOLUHCLGIKXWDMXKGPDCBMWKFFKKMSIQWITRAIPRAFMULFYHMCTMRCLQAKXOLUWWQRADXVTRYDXVQMXRAWMHVQZESYMBLPSPULNKMFHKMPNZVZKEXBNUMCLQAEMNMMRGIAFHIPVCLXYQKPUKEZOXAEHNDVYXEWDZYWMSIAWRYNKFBFYIPRANHTNMRNHITDVCLXYNDRMNUUYYMBLQDYHAXDHFKKCBLZDREZQNTUYYMKWVUBTABKIQIMXKWMUZVZKEXBNXMBSKMHXDHFK"
simmulated_annealing(problem_2_encrypted_string)

key = "KGGIKGYUYKCIVUVZGIMBWQVBKCLQCIRAGKOVKFRANDVYXEWDZY"
print(playfair_decrypt())