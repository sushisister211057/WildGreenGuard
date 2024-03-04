import json

trans_dict = {
    # 物種
    "Ageratum_houstonianum":["紫花藿香薊","Flossflower","ムラサキカッコウアザミ"],
    "Bidens_pilosa_var_radiata":["大花咸豐草","Pilose Beggarticks","タチアワユキセンダングサ"],
    "Bryophyllum_pinnatum":["落地生根","Life plant","セイロンベンケイ"],
    "Chloris_barbata":["孟仁草","Swollen finger grass","クロリス・バルバタ"],
    "Conyza_species":["加拿大蓬","Horseweed","ヒメムカシヨモギ"],
    "Crassocephalum_crepidioides":["昭和草","Redflower ragleaf","ベニバナボロギク"],
    "Lantana_camara":["馬纓丹","Common lantana","ランタナ"],
    "Leucaena_leucocephala":["銀合歡","River tamarind","ギンネム"],
    "Mikania_micrantha":["小花蔓澤蘭","Bitter vine","ツルヒヨドリ"],
    "Pennisetum_purpureum":["象草","Napier grass","ナピアグラス"],
    "Rhynchelytrum_repens":["紅毛草","Natal Grass","ルビーガヤ"],
    "Syngonium_podophyllum":["合果芋","Arrowhead Plant","シンゴニウム・ポドフィラム"],
    "Tithonia_diversifolia":["王爺葵","Tree marigold","ニトベギク"],
    "Eleusine_indica":["牛筋草","Goosegrass","オヒシバ"],
    "Cynodon_dactylon":["狗牙根","Bermuda Grass","ギョウギシバ"],
    "Miscanthus_species":["芒草","Silver grass","ススキ"],
    "Amaranthus_spinosus":["刺莧","Pilose Beggarticks","ハリビユ"],
    "Celosia_argentea":["雞冠花","Silver cock's comb","セロシア"],
    "Cardiospermum_halicacabum":["倒地鈴","Balloon vine","フウセンカズラ"],
    # 植物圖鑑資訊
    # 紫花藿香薊
    "ahdes":["高30-100公分，葉子呈現鈍三角形或心形，\n分布於全台低海拔至1,300公尺地區。","It is an annual plant with a height ranging from 30 to 100 cm.\nThe leaves are ovate to triangular-ovate, with a length of 2 to 7 cm, having a blunt apex and a shallow heart-shaped base.\nThe edges of the leaves are serrated. It is distributed in regions with an elevation of up to 1,300 m.","高さ30-100 cmの一年草である。\n葉は長さ2-7 cmの卵形～三角状卵形、鈍頭で、基部は浅い心形となり、縁には鋸歯がある。\n標高1,300 m以下の地域に分布してる。"],
    # 刺莧
    "asdes":["高30-100公分，花為綠色，分布於全台田地。","The plant reaches a height of approximately 30 to 100 cm. The flower color is green.\nIt is distributed throughout Taiwan, particularly commonly found around cultivated fields.","草丈は30-100 cmほどになる。花の色は緑である。\n台湾全域に分布してる。特に畑地の周辺で多く見られる。"],
    # 大花咸豐草
    "bpvrdes":["高可達2公尺，開花期長，對天災耐性強，\n分布於全台低海拔至1,000公尺地區。","The plant reaches a height of 2m, blooms throughout the year, and is highly resistant to natural disasters.\nIt is distributed in low-altitude areas throughout Taiwan, up to an elevation of 1,000 m.","高さが2 mに達し、通年で開花し、環境ストレスに対する耐性が非常に高い植物であり、\n標高1,000 m以下の地域に分布してる。"],
    # 雞冠花
    "cades":["又稱青葙，高30-100公分，\n花為圓柱狀，顏色白色或紫紅色，分布於全台低海拔地區。","Commonly known as plumed cockscomb, it grows to a height of 30 to 100 cm,\nwith cylindrical-shaped flowers in white or purplish-red.It is distributed in low-altitude areas throughout Taiwan.","「ノゲイトウ」とも呼ばれ、高さ30-100 cmで、\n花は円柱状で、白色または赤紫色である。標高の低い地域に分布してる。"],
    # 孟仁草
    "cbdes":["高30-120公分，花為穗狀花序，顏色呈紫紅色。\n分布於全台低海拔和海邊地區。","It grows to a height of 30 to 120 cm, with spike-like inflorescences in a purplish-red color.\nIt is distributed in low-altitude and coastal areas throughout Taiwan.","草丈は30-120 cmほどになる。穂状花序であり、花の色は赤紫色である。\n標高の低い地域や海沿いに分布してる。"],
    # 昭和草
    "ccdes":["高可達1公尺，花為紅褐色，分布於全台低至中海拔開闊地區。","It reaches a height of up to 1 meter, with flowers in a reddish-brown color,\nand is distributed in broad regions at low to mid-altitudes throughout Taiwan.","高さが1 mに達し、花の色はレンガ色である。\n標高2,400 m以下の広い地域に分布してる。"],
    # 狗牙根
    "cddes":["高約15-25 公分，稈斜上或直立，分布於全台平地及丘陵地區。","It is approximately 15-25 cm tall, with stems that are inclined or erect.\nIt is distributed in plains and hilly areas throughout Taiwan.","高さは約15-25 cmで、茎は斜めまたは直立しており、\n全台の平地および丘陵地域に分布してる。"],
    # 牛筋草
    "eides":["根系深入土內，不易拔除，穗狀花序長3-9公分，全台都有生長。","The roots penetrate deeply, making it hard to remove.\nIt has a spike-like inflorescence, with the flower cluster measuring 3-9 cm in length,\nand it is distributed throughout Taiwan.","根が深く入り、引き抜きにくい。\n穂状花序であり、花序は3-9 cmの長さで、広い地域に分布してる。"],
    # 馬纓丹
    "lcdes":["葉子為楔形或略心形，花顏色多變、形狀為球形，\n分布於全台低海拔地區。","The leaves are wedge-shaped or heart-shaped.\nWith ball-shaped flowers, the corolla color is extremely diverse in Common lantana.\nIt is distributed in low-altitude throughout Taiwan.","葉の基部はくさび形～心形である。\n花色は多様で、ボール状に花が咲く。\n標高の低い地域に分布してる。"],
    # 銀合歡
    "lldes":["高可達10公尺，莢果長10-15公分，種子褐色，光滑具光澤，\n分布於全台3,000公尺以下地區。","It reaches a height of up to 10 m, with pods measuring 10-15 cm in length.\nThe seeds are brown, smooth, and shiny.\nIt is distributed in areas below 3,000 m altitude throughout Taiwan.","高さが10 mに達し、果実は10-15 cmの長さで、茶色の豆果であり、滑らかで光沢がある。\n標高3,000 m以下の地域に分布してる。"],
    # 小花蔓澤蘭
    "mmdes":["花冠為白色，葉子心形，莖細長，匍匐或攀緣，\n分布於全台至中低海拔1,000公尺地區。","The corolla is white, leaves are heart-shaped.\nThe stems are slender and long, usually climbing and twining around other objects.\nIt is distributed in areas below 1,000 m altitude throughout Taiwan.","花は白い小さな頭花をまとまった花序にして付ける。\n葉はハート形で、茎は細長く、他のものに絡みついて這い上がる。\n標高1,000 m以下の地域に分布してる。"],
    # 象草
    "ppdes":["高可達3公尺，細小剛毛摸起來柔軟舒適，\n分布於全台平地至中海拔1,500公尺地區。","It reaches a height of up to 3 m.\nThe inflorescence is a stiff terminal bristly spike, with a soft texture.\nIt is distributed in areas below 1,500 m altitude throughout Taiwan.","高さが3 mに達し、細かい剛毛があり触ると柔らかく快適で、\n標高1,500 m以下の地域に分布してる。"],
    # 芒草
    "msdes":["高約1-3公尺，花初期為淡黃色，分布於全台低海拔地區。","It reaches a height of approximately 1 to 3 m.\nDuring the start of the flowering stage, the inflorescence color presents as pale yellow.\nIt is distributed in low-altitude regions throughout Taiwan.","高さが約1-3 mで、穂が出始めた頃は淡黄色である。\n標高の低い地域に分布してる。"],
    # 合果芋
    "spdes":["葉子箭頭形，具攀附性，顏色白、綠相間，\n分布於全台北部低海拔地區。","With its arrowhead-shaped leaves, this climbing plant exhibits a lovely leaf color featuring a mix of white and green.\nIt is commonly found in low-altitude areas in northern Taiwan. ","葉は矢じり形で、つる性植物である。\nホワイトグリーン色のような綺麗な葉色をしてる。\n台湾北部の低標高地域に分布してる。"],
    # 王爺葵
    "tddes":["高可達3公尺，花瓣黃色，分布於全台至中低海拔地區。","It reaches a height of up to 3 m and has yellow petals.\nIt is distributed throughout Taiwan in low to mid-altitude areas.","高さが3 mに達し、黄色い花である。\n標高2,400 m以下の地域に分布してる。"],
    # Line bot圖文選單
    "qa":["常見問題","FAQ","FAQ"],
    "dev":["開發人員","Developers","開発者"],
    "web":["網頁","Website","Webサイト"],
    "idplant":["外來種植物辨識","Identify Invasive Plants","外来種植物を識別する"],
    "history":["歷史紀錄查詢","Search History","履歴を検索する"],
    # Line bot 外來種植物辨識對話
    "oneimg":["唉呀，只能傳一張植物照片，不可以貪心哦！","Oops, only one plant picture at a time.","アップできるのは一度に一枚の写真だけだよ。"],
    "upaimg":["請上傳一張植物圖片","Please upload a picture of the plant.","一枚の植物の画像をアップロードしてね"],
    "upimg":["上傳圖片","Upload a picture","画像をアップロード"],
    "cameraon":["開啟相機","Turn on the camera","カメラを開く"],
    "idsuc":["太棒了！[人名]\n你用得很得心應手嘛!\n這就是[植物名]。\n如果還有其他的植物，也別忘了和我分享哦！","Wow, [人名]\nYou nailed it!\nThis is [植物名].\nIf there are any other plants, please don’t hesitate to share them with me!","やったね！[人名]\nうまくいったよ！\nこれが[植物名]だよ。\n他にも面白い植物があれば、ぜひ教えてくれるとうれしいな！"],
    "idfail":["哎呀，辨識失敗了嗎？\n不要灰心，你可以試試換個角度拍攝，再傳給我圖片，我再幫你看看","Oh dear, the plant can't be found.\nCould you please take another photo and give it another try?","あらら、植物が見つからなかった。\nもう一度写真を取り直してみてくれる？"],
    "idagain":["是否再次辨識植物","Would you like to identify the plants again?","もう一度植物を識別する？"],
    "thxuse":["感謝你使用WildGreenGuard!\n如果還有其他的植物，別忘了和我分享哦！","Thank you for using WildGreenGuard.\nIf there are any other plants, please don’t hesitate to share them with me!","WildGreenGuardをご利用いただきありがとうございます。\n他にも面白い植物があれば、ぜひ教えてくれるとうれしいな！"],
    "y":["是","Yes","はい"],
    "n":["否","No","いいえ"],
    # Line bot 歷史紀錄查詢對話
    "norec":["沒有任何歷史紀錄喔!","No history records found!","履歴が見つからなかったよ!"],
    "species":["植物名稱","Plant name","植物名"],
    "sciname":["學名","Scientific name","学名"],
    "uptime":["圖片上傳時間","Time of picture upload","アップロードした時間"],
    "prehis":["是否再查看先前的歷史紀錄","Would you like to check the previous history?","もう一度過去の履歴を見る？"],
    "vimgin":["查看更多資訊","View more info","詳細を見る"],
    "enjimg":["好好欣賞植物圖片吧!","Enjoy the beauty of the uploaded plant images!","アップロードされた植物の画像の美しさをお楽しみくださいね！"],
    "clvimgin":["點選上方的「查看更多資訊」吧!","Click on 'View More Info' above!","上の「詳細を見る」をタップしてね！"],
    "disother":["是否再顯示其他的植物種類?","Would you like to see additional plant species?","他の植物種も表示するか？"],
    "curhis":["目前歷史紀錄裡只有上面的植物種類喔！","The current history record only contains plant species as above!","現在の履歴には上記の植物種のみが含まれている！"],
    "dl":["下載","Download","ダウンロード"],
    # Line bot 網頁
    "weblog":["想立即前往網站或獲取登入資訊於電腦端登入使用?","Would you like to visit the website immediately or obtain login information for logging in by computer?","Webサイトをすぐに訪れるか、それともコンピュータでログインするためのログイン情報を取得する？"],
    "visweb":["前往網頁","Visit the website","Webサイトを訪れる"],
    "loginfo":["登入資訊","Obtain login info","ログイン情報を取得する"],
    # 網頁
    "yolo":["YOLO影像辨識","YOLO Image Identification","YOLO画像識別"],
    "data":["植物資料庫","Plant Database","植物データベース"],
    "record":["植物辨識紀錄","Plant Identification records","植物識別履歴"],
    "dt":["資料","Data","データ"],
    "about":["關於","About","情報"],
    "cameraoff":["關閉相機","Turn off the camera","カメラを閉じる"],
    "selectf":["選擇圖片","Select the picture","画像を選択"],
    "confirm":["確認","Upload","完了"],
    "member":["成員","Members","メンバー"],
    "scanqr":["掃描QR code註冊","Scan QR code to register","QR コードをスキャンして登録"],
    "psi":["請登入","Please sign in","サインインしてください"],
    "id":["使用者代號","Userid","ユーザID"],
    "username":["使用者名稱","Name","ユーザー名"],
    "signin":["登入","Sign in","サインイン"],
    "signout":["登出","Sign out","サインアウト"],
    "login_error":["輸入的使用者代碼或使用者名稱有誤，或是用linebot的網頁按鈕重新取得登入資訊。","The entered userid or username is incorrect, or you can obtain login information again by tapping the Line Bot Website button.","入力されたユーザーIDまたはユーザー名が正しくありません。または、Line BotのWebサイトボタンをタップしてログイン情報を再取得できます。"],
    "insp":["外來種","Invasive Species","外来種"],
    "nasp":["非外來種","Native Species","在来種"],
    "res":["結果","Result","結果"],
    # 網頁介紹
    "webintro":["是一款以台灣入侵種為主題的外來種植物圖片辨識網站，兼具line機器人服務平台，\n有中英日文切換功能，操作簡單、使用便利。\n選單中的「植物資料庫」列出可辨識的植物物種。如有操作上的疑問，可以查閱「常見問題」以獲得解答。","It is a website designed to identify invasive plant species in Taiwan, featuring a Line Bot platform.\nIt supports Chinese, English, and Japanese and provides a user-friendly experience.\nThe “Plant Database” lists plant species that can be identified by WildGreenGuard.\nFor any inquiries, please refer to the “FAQ” section.","WildGreenGuard は台湾の外来種植物を識別するためのウエブサイトであり、Line Bot を備えている。\n中国語、英語、日本語3言語に対応しており、使いやすいサービスを提供している。\nメニューの「植物データベース」では、識別可能な植物の種類を一覧にしている。\nご不明点がある場合は「FAQ」をご参照ください。"],
    "intro":["這是一個辨識台灣外來種植物的網站","It is a website designed to identify invasive plant species in Taiwan.","台湾の外来植物を識別するためのウエブサイトである。"],
    # 常見問題
    "q1":["1. 可辨識的植物有哪些?","1. What kind of plants can WildGreenGuard identify?","1. WildGreenGuardはどの種類の植物を識別できる？"],
    "a1":["可參考網頁版的「植物資料庫」，裡面列出可辨識的植物種類及植物簡介。","You can refer to the web version of “Plant Database”,\nwhich lists plant species that can be identified by WildGreenGuard and provides plant introductions.","「植物データベース」のウエブ版を参考にしてください。\nこちらでは、WildGreenGuardによって識別可能な植物種とその植物の一覧を掲載してる。"],
    "q2":["2. 若無法讀取植物辨識結果該怎麼辦?","2. Why is plant image recognition not successful?","2. どうして画像がうまく認識されない?"],
    "a2":["上傳的植物圖片需在陽光充足的環境下拍攝，且畫面須清晰不模糊。\n也可上傳不同拍攝角度的植物圖片以利辨識。","The uploaded plant photos should be taken in well-lit conditions, and the images must be clear.\nUploading images from different angles would improve the success rate of recognition.","画像が鮮明でない場合、正しい検索結果が表示されない場合があります。\n明るい環境での撮影と撮影する角度や位置を変更することをおすすめします。"],
    "q3":["3. 如何獲得網頁版的登入資訊?","3. How to obtain the login information for the web version?","3. ウエブ版のログイン情報をどうのように取得できる？"],
    "a3":["點選Line bot的「網頁」功能，並按「登入資訊」即可獲得使用者代碼及使用者名稱。","Tap on the ‘Web’ option within the Line bot’s rich menu, then select ‘Login info’  to obtain the user ID and username.","Line ボットのリッチメニューで「Web」をタップし、「ログイン情報を取得する」を選択して、ユーザーIDとユーザー名を取得できる。"],
    "q4":["4. 使用YOLO影像辨識時，如何減少結果中方框的重疊?","4. How to reduce the overlap of bounding boxes in the results when using YOLO Image Identification?","4. YOLO画像識別を使用する際、出力結果の重なったバウンディングボックスを減らす方法がある？"],
    "a4":["使用YOLO影像辨識時，建議讓畫面中植物特徵不要複雜，減少方框的產生，以便更容易進行辨識。","When using YOLO Image Identification, it is recommended to focus on scenes with a single plant feature,\nreducing the occurrence of bounding boxes for better identification.","YOLO画像識別を使用する際には、画面中の植物特徴をシンプルに保つことをお勧めし、\nバウンディングボックスの生成を減らすことで、よりスムーズな識別が可能となる。"],
    # 
    # 人名
    "ZJM":["張家銘","ZHANG, JIA-MING","ちょうかめい"],
    "ZYT":["張雅婷","ZHANG, YA-TING","ちょうがてい"],
    "ZDQ":["張大謙","ZHANG, DA-QIAN","ちょうだいけん"],
    "HGT":["何耿廷","HE, GENG-TING","かこうてい"],
    "LCH":["梁鈞翔","LIANG, CHUN-HSIANG","りょうきんしょう"],
    "LXW":["呂星緯","LU, XING-WEI","りょせいい"],
    "HTC":["許庭瑊","HSU, TING CHEN","きょていしん"],
}

# print(json.dumps(trans_dict))

# # 上述內容自己產生json檔案
with open("translate.json","w", encoding="utf-8") as f:
    f.write(json.dumps(trans_dict, ensure_ascii=False, indent=4))


#
# with open("translate.json","r") as f :
#     text_open = f.read()

# # text_open = json.loads("translate.json")

# print(text_open)
# print(type(text_open))

# dict_text= json.loads(text_open)
# print(dict_text)
# print(type(dict_text))
