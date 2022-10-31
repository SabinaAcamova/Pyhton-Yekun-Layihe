import curses # curses library metnin rengini ve uslubunu deyismeye imkan verir. Metni qalın,highlightlı, vurğulanmış, altından xett çeke ve reng deyise bilerik
from curses import wrapper #mən bu wrapperde cursesi işə salmaq üçün istifadə edirəm və sonra proqramı bitirən kimi o, terminalı əvvəlki vəziyyətinə qaytaracaq.
import time # Python-da vaxtla işləməyə imkan verir. O, cari vaxtı əldə etmək, Proqramın icrasını dayandırmaq və s. kimi funksiyalara imkan verir.
import random #təsadüfi nömrələr yaratmaq, siyahı və ya sətir üçün təsadüfi dəyəri çap etmək kimi təsadüfi hərəkətləri yerinə yetirmək üçün istifadə edilir


def start_screen(stdscr): #start_screen funksiyasi. curses modulun methodlarina erisim ucun (stdscr) yazilir
	stdscr.clear() # butun ekranı təmizləyir
	stdscr.addstr("Welcome to the Speed Typing Test!") #ekrana 'Welcome to the Speed Typing Test!' yazir
	stdscr.addstr("\nPress any key to begin!") #ekrana 'Press any key to begin!" yazir \n-new line 
	stdscr.refresh()# butun ekrani yenileyir
	stdscr.getkey()#proqrami derhal baglamir, istifadecinin bir sey daxil etmesini gozleyir. Eger getkey() yazmasaq yuxarda yazilanlar print olunduqdan derhal sonra silinecek(millisecond).

def display_text(stdscr, target, current, wpm=0): #display_text funksiyasi. stdscr, target, current, wpm=0 parametrlərdir, yəni biz onu çağırdığımız zaman bu funksiyaya dəyərlər ötürməliyik. wpm=optional parameter
	stdscr.addstr(target) #target parametri cap olunur
	stdscr.addstr(1, 0, f"WPM: {wpm}") #1,0 koordinatlar. f"WPM: {wpm}-iki sətir əlavə etmədən python ifadələrini birbaşa sətirin içərisinə yerləşdirməyə imkan verir.
    # bu hissede current textimin target textin uzerine yazilmasini isteyirem
	for i, char in enumerate(current): #enumerate ile current textdeki elementleri ve onlarin indexlerini verir (i-index, char-character)
		correct_char = target[i] # target parametrindeki her bir elementin indexini correct_char-a atayiriq
		color = curses.color_pair(1) # curses.color_pair(1)-ı bir degiskende saxlayiriq or degisken atayiriq. 1-main funkda yazdigimiz yasil rengin ID-si
		if char != correct_char: #eger daxil etdiyimiz element menim target textimdeki elemente beraber olmasa reng qirmiziya cevrilir
			color = curses.color_pair(2) #curses.color_pair(2)-ı bir degiskende saxlayiriq. 2-main funkda yazdigimiz qirmizi rengin ID-si

		stdscr.addstr(0, i, char, color) #0, i textin koordinatlari. char, color variable (print olunur)

def load_text(): #load_text funksiyasi
	with open("text.txt", "r") as f: #faylimizi aciriq. "r"-faylları oxumaq və məlumatlari əldə etmək.Fayldaki melumatlar f de saxlanilir
		lines = f.readlines() #.readlines()-faylda her bir linedeki yazilardan ibaret list verir
		return random.choice(lines).strip() #listden random 1 element secir. .strip() isimizi asanlasdirir faylda her setrin sonuna \n yazmali qalmiriq

def wpm_test(stdscr): #wpm_test funksiyasi. curses modulun methodlarina erisim ucun (stdscr) yazilir
	target_text = load_text() #load_text funksiyasi target_texte atanir ve funksiya cagirilir
	current_text = [] #current_text adinda empty list yaradiriq (key = stdscr.getkey() de userin daxil etdiyi char bu listde olacaq )
	wpm = 0 #wpm-in baslangic qiymeti
	start_time = time.time() #bu üsul dövrdən bəri saniyələrlə vaxtı əks etdirən float dəyərini qaytarır ve bunu start_time-a atayiriq
	stdscr.nodelay(True) #istifadəçinin düyməyə basmasını gözləməyi gecikdirmemek
     #wpm-in hesablanib ekrana print olunmasi ucun dongu
	while True:
		time_elapsed = max(time.time() - start_time, 1) # indiki vaxtdan baslangic vaxti cixsaq bize qalan vaxti verir. max ve 1 ona gore yazilirki zero division xetasi vermesin
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5) #wpm-in tapilma dusturu.Eger eded decimaldirsa onda round ile yuvarlaqlasdirir

		stdscr.clear()  # butun ekranı təmizləyir
		
		display_text(stdscr, target_text, current_text, wpm) #call display_text func. stdscr, target_text, current_text, wpm parametrlərdir, yəni biz onu çağırdığımız zaman bu funksiyaya dəyərlər ötürməliyik
		stdscr.refresh() # butun ekrani yenileyir

		if "".join(current_text) == target_text: #current_text listini stringe ceviririk. join() metodu bütün elementləri iterativ olaraq götürür və onları bir sətirdə birləşdirir.
			stdscr.nodelay(False) #Mən ekranda bir şey göstərmək istəyirəm və sonra davam etməzdən əvvəl istifadəçinin düyməni vurmasını gözləmək istəyirəm

			break # dövru dayandırmaq və dövrden sonra növbəti koda keçmək ucun
        #eger user hec bir duymeye basmasa helede wpmin azaldigi ekranda gorsenmelidir. Ona gore try except bloklarindan istifade edirik. User hec bir sey daxil etmese kod dongunun evveline qayidir. Buda bize wpmin azaldigini gosterir
		try:
			key = stdscr.getkey() #stdscr.getkey()-i bir degiskende saxlayiriq or degisken atayiriq
		except:
			continue

		if ord(key) == 27: #eger bizim ordinal valuemiz 27 e beraberdise break edir. ASCII 27 = escape 
			break # dövru dayandırmaq və dövrden sonra növbəti koda keçmək ucun
# backspace-e basanda yazdigim metnin silinmesini  isteyirem ona gore
		if key in ("KEY_BACKSPACE", '\b', "\x7f"): #backspace bu ucu ile temsil oluna biler. Eger key bu 3-den birine beraber olarsa
			if len(current_text) > 0: #current_textin uzunlugu 0-dan boyuk oldugu muddetce
				current_text.pop() #biz backspace-e basanda .pop() dan istifade ederek curren_textde son daxil etdiyimiz elementi silecek
		elif len(current_text) < len(target_text): # curren_text deki elementlerin sayi target_text den cox ola bilmez. az oldugu muddetce asagidaki kod isleyir
			current_text.append(key) #istifadəçinin basdığı ​​bütün düymələrin siyahısı (userin daxil etdiyi charlar append funk vasitesile liste daxil olur)


def main(stdscr):#main func stdscr-ekrana birşeylər yazmağa imkan verir
	#add color to our text
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #init_pair(n, f, b)  n-ID(1) f-yazinin rengi(yasil) b-arxaplan rengi(qara)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)#init_pair(n, f, b)  n-ID(2) f-yazinin rengi(qirmizi) b-arxaplan rengi(qara)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)#init_pair(n, f, b)  n-ID(3) f-yazinin rengi(ag) b-arxaplan rengi(qara)

	start_screen(stdscr) #call start_screen func
	#bu dongu her defe yeniden davam etmek ucundur. esc duymesine basildigda bu donguden cixir
	while True: 
		wpm_test(stdscr) #call wpm_test func
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue...") #2-column 0-row yazinin koordinatlaridir ve "You completed the text! Press any key to continue..." print olunur
		key = stdscr.getkey() #stdscr.getkey()-i bir degiskende saxlayiriq or degisken atayiriq
		
		if ord(key) == 27: #eger bizim ordinal valuemiz 27 e beraberdise break edir. ASCII 27 = escape 
			break # dövru dayandırmaq və dövrden sonra növbəti koda keçmək ucun

wrapper(main) #call wrapper
