import curses  # curses library metnin rengini ve uslubunu deyismeye imkan verir. Metni qalın,highlightlı, vurğulanmış, altından xett çeke ve reng deyise bilerik
from curses import wrapper #mən bu wrapperde cursesi işə salmaq üçün istifadə edirəm və sonra proqramı bitirən kimi o, terminalı əvvəlki vəziyyətinə qaytaracaq.
import queue #Python-da biz obyektlərin növbəsini yaratmaq üçün queue modulundan istifadə edirik
import time # Python-da vaxtla işləməyə imkan verir. O, cari vaxtı əldə etmək, Proqramın icrasını dayandırmaq və s. kimi funksiyalara imkan verir.

# " "- Yol, 'H'-Maze-in divarlari, B-baslangic noqtesi, E- bitis noqtesi
maze = [
    ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", " ", " ", " ", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],
    ["H", " ", "H", "H", " ", " ", " ", " ", " ", " ", " ", "H", "H", " ", "H", " ", " ", " ", "H", " ", "H", "H", " ", " ", " ", " ", " ", " ", " ", "H", "H", " ", "H"],
    ["H", " ", " ", " ", " ", "H", "H", "H", " ", "H", "H", " ", " ", " ", "H", " ", " ", " ", "H", " ", " ", " ", " ", "H", "H", "H", " ", "H", "H", " ", " ", " ", "E"],
    ["H", " ", "H", " ", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", "H"],
    ["H", " ", "H", " ", " ", "H", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", " ", "H", "H", " ", "H", " ", " ", " ", "H", " ", "H"],
    ["H", " ", "H", "H", " ", "H", "H", " ", "H", "H", " ", " ", "H", "H", "H", " ", " ", " ", "H", " ", "H", "H", " ", "H", "H", " ", "H", "H", " ", " ", "H", "H", "H"],
    ["H", " ", "H", "H", " ", " ", "H", " ", "H", " ", "H", " ", "H", " ", "H", "H", "H", "H", "H", " ", "H", "H", " ", " ", "H", " ", "H", " ", "H", " ", "H", " ", "H"],
    ["H", " ", " ", " ", "H", " ", " ", " ", " ", " ", " ", " ", "H", " ", " ", " ", " ", " ", " ", " ", " ", " ", "H", " ", " ", " ", " ", " ", " ", "H", " ", " ", "H"],
    ["H", " ", "H", " ", " ", " ", "H", " ", " ", "H", "H", "H", " ", " ", "H", "H", "H", "H", "H", " ", "H", " ", " ", " ", "H", " ", " ", "H", "H", "H", " ", " ", "H"],
    ["H", " ", "H", " ", " ", "H", " ", "H", " ", " ", " ", "H", "H", " ", "H", " ", " ", " ", "H", " ", "H", " ", " ", "H", " ", "H", " ", " ", " ", "H", "H", " ", "H"],
    ["H", " ", " ", " ", "H", "H", "H", "H", " ", "H", " ", "H", " ", " ", "H", " ", " ", " ", "H", " ", " ", " ", "H", "H", "H", "H", " ", "H", " ", "H", " ", " ", "H"],
    ["H", " ", "H", " ", "H", "H", " ", "H", " ", "H", " ", "H", " ", " ", "H", " ", " ", " ", "H", " ", "H", " ", "H", "H", " ", "H", " ", "H", " ", "H", " ", " ", "H"],
    ["H", " ", "H", "H", " ", "H", " ", " ", "H", "H", " ", " ", " ", " ", "H", " ", " ", " ", "H", " ", "H", "H", " ", "H", " ", " ", "H", "H", " ", " ", " ", " ", "H"],
    ["B", " ", " ", "H", " ", "H", " ", "H", " ", " ", " ", " ", " ", "H", "H", " ", " ", " ", "H", " ", " ", "H", " ", "H", " ", "H", " ", " ", " ", " ", " ", "H", "H"],
    ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", " ", " ", " ", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H"]
]

# labirinti ekrana cap eden funksiya
def print_maze(maze, stdscr, path=[]): # print_maze func. maze, stdscr, path=[] parametler
    #maze-in rengleri
    CYAN = curses.color_pair(1) #curses.color_pair(1)-ı CYAN degiskeninde saxlayiriqki istifade edek. 1-main funkda yazdigimiz cyan rengin ID-si
    YELLOW = curses.color_pair(2) #curses.color_pair(2)-ı YELLOW degiskeninde saxlayiriqki istifade edek. 2-main funkda yazdigimiz sari rengin ID-si

    for i, row in enumerate(maze): #enumerate() funksiyasından istifadə etdiyiniz zaman mazedeki iki döngə dəyişənini i ve row-u geri qaytarır.
        for j, value in enumerate(row): #enumerate() funksiyasından istifadə etdiyiniz zaman rowdaki iki döngə dəyişənini j ve value-u geri qaytarır.bu hissede j columnu temsil edir
            if (i, j) in path: #eger i,j path-in daxilindedirse
                stdscr.addstr(i, j*2, "E", YELLOW) #i,j position(row,column). j*2- columnu arali cap edir. YELLOW E-in rengi/ getdiyimiz yolun rengi
            else:
                stdscr.addstr(i, j*2, value, CYAN) #i,j position(row,column). j*2- columnu arali cap edir. CYAN-"H"

#baslangicin koordinatini tapmaq ucun istifade olunur
def find_start(maze, start): #find_start func. ve parametrleri
    for i, row in enumerate(maze):  #enumerate() funksiyasından istifadə etdiyiniz zaman mazedeki iki döngə dəyişənini i ve row-u geri qaytarır.
        for j, value in enumerate(row):#enumerate() funksiyasından istifadə etdiyiniz zaman rowdaki iki döngə dəyişənini j ve value-u geri qaytarır.bu hissede j columnu temsil edir
            if value == start: # value starta yeni B-e beraber olarsa
                return i, j # koordinati qaytarir

    return None # B tapilmazsa None


def find_path(maze, stdscr): #find_path func. ve parametrleri
    #baslangic ve son noqtelerimizin hara oldugunu teyin edirik
    start = "B" #baslangic noqtesi B-ni start-a atayiriq
    end = "E" #bitis noqtesi E-i end-e atayiriq
    start_pos = find_start(maze, start) #call find_start func ve baslangic noqtesinin koordinatlarini start_pos-a atayiriq 

    q = queue.Queue() #queue modulundan istifade etmek ucun q-e atayiriq  .Queue()- queue modulunun tətbiq üsullarından biridir
    q.put((start_pos, [start_pos])) #put() metodu növbəyə element əlavə edir
    #current_pos = start_pos, path = [start_pos]

    visited = set() #ziyarət etdiyimiz bütün mövqeləri özündə cəmləşdirən ziyarət edilmiş dəst yaradiriq

    while not q.empty(): #empty() metodu Queue instansiyasında hər hansı elementin olub-olmadığını yoxlayır. Növbədə heç bir element olmadıqda True qaytarır. Əks halda False qaytarır
        current_pos, path = q.get() #get() metodu açar lüğətdə olarsa, göstərilən açarın dəyərini qaytarır. onuda current_pos,path e atayiriq
        row, col = current_pos #current positionu row ve columna atayiriq

        stdscr.clear()  # butun ekranı təmizləyir
        print_maze(maze, stdscr, path) #call print_maze func
        time.sleep(0.2) #yolu tapmanin gedisatini gormek ucun yavasladiriq
        stdscr.refresh() # butun ekrani yenileyir

        if maze[row][col] == end: #Əgər bu mövqe E-ə bərabərdirsə, odursa, o deməkdir ki, biz qisa yolu tapmışıq.
            return path # path-i qaytarir
        #chechk obstacles
        neighbors = find_neighbors(maze, row, col) #call find_neighbors func ve neighbors-a atayiriq
        for neighbor in neighbors: #for döngüsü ile neighbors listesi üzerindeki her bir elemente catiriq ve neighbor değişkeninin içerisine kopyaliyiriq
            if neighbor in visited: #eger neighbor ziyaret etdiyimiz butun movqelerin daxilindedirse
                continue 

            r, c = neighbor  #(r,c=row,column) neighbor-u row ve columna atayiriq
            if maze[r][c] == "H": #eger maze-de r,c "H" isaresine beraber olarsa 
                continue 

            new_path = path + [neighbor] #burada neighboru listin icinde yaziriq cunki 2 listi toplayiriq ve cemi new_path-a atayiriq
            q.put((neighbor, new_path)) ##put() metodu növbəyə element əlavə edir
            visited.add(neighbor) # add() metodu verilmiş elementi yeni neighbor-u visited-e əlavə edir

#butun qonsulari tapmaq ucun funksiya
def find_neighbors(maze, row, col): #find_neighbors func. ve parametrleri
    neighbors = [] #neighbors adli empty list yaradiriq

    if row > 0:  # UP eger row>0 olarsa
        neighbors.append((row - 1, col)) #bu zaman neighbors siyahisina row-un 1 evvelki veziyyeti ve column liste elave olunur
    if row + 1 < len(maze):  # DOWN  row + 1 < len(maze) olarsa
        neighbors.append((row + 1, col)) #bu zaman rowdan 1 sonraki veziyyet ve column liste elave olunur
    if col > 0:  # LEFT eger col > 0 olarsa
        neighbors.append((row, col - 1))# row, columndan 1 evvelki veziyyet liste elave olunur
    if col + 1 < len(maze[0]):  # RIGHT 
        neighbors.append((row, col + 1)) #row, columndan 1 sonraki veziyyet liste elave olunur

    return neighbors #neighbors qaytarir


def main(stdscr): #main func stdscr-ekrana birşeylər yazmağa imkan verir
    #add color to our text
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) #init_pair(n, f, b)  n-ID(1) f-yazinin rengi(cyan) b-arxaplan rengi(qara)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) #init_pair(n, f, b)  n-ID(1) f-yazinin rengi(sari) b-arxaplan rengi(qara)

    find_path(maze, stdscr) #call find_path func
    stdscr.getch() #bunun mənası xarakter almaqdır. Userin ne ise daxil etmesini gozleyir


wrapper(main) #call wrapper