import tkinter as tk #importē Tkinter bibliotēku un nosaukumu tk
import requests #importē requests bibliotēku
import json #importē json bibliotēku
import tokens #importē tokens moduli

def search_spotify(): #funkcija search_spotify
    #piekļuve potify API access token
    access_token = tokens.get_token()

    #noskaņojuma ievade
    mood = mood_entry.get()

    root.geometry("665x530") #uzstāda loga izmēru

    #meklē dziesmas atbilstoši noskaņojumam
    headers = {
        "Authorization": "Bearer " + access_token
    }
    query = mood + " playlist"
    params = {
        "q": query,
        "type": "playlist",
        "limit": 1
    }
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    #izvelk playlist ID
    data = json.loads(response.text)
    if "playlists" in data and data["playlists"]["total"] > 0:
        playlist_id = data["playlists"]["items"][0]["id"]
    else:
        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, "No playlists found based on your mood. Please try again with a different mood.")
        return

    #saņem playlist dziesmas
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
    data = json.loads(response.text)

    #atjaunina label ar playlist dziesmām
    results_text.delete('1.0', tk.END)
    results_text.insert(tk.END, "100 songs based on your mood:\n")
    for i, item in enumerate(data["items"]):
        results_text.insert(tk.END, f"{i+1}. {item['track']['name']} by {item['track']['artists'][0]['name']}\n")

#GUI grafiskā lietotāja saskarne
root = tk.Tk() #izveido Tk objektu un saglabā to mainīgajā root
root.geometry("665x530") #loga izmērs
root.configure(bg='lightblue')
root.title("100 songs based on your mood") #loga virsraksts
root.eval("tk::PlaceWindow . center") #novieto logu ekrāna centrā
root.resizable(False, False) #neļauj mainīt loga izmēru
l1 = tk.Label(root,  text='Enter your mood (e.g. happy, sad, romantic, etc.):', bg='lightblue', padx=90) #izveido uzrakstu ar norādījumu "ievadīt noskaņojumu"
l1.grid(row=1,column=1,padx=90)

#ievades lauks noskaņojumam un meklēšanas pogai
mood_entry = tk.Entry(root)
mood_entry.grid(row=2,column=1,padx=90)
search_button = tk.Button(root, text="Search", command=search_spotify)
search_button.grid(row=3,column=1,padx=90)

#label rezultātu parādīšanai
l2 = tk.Label(root,  text='Songs based on your mood:', padx=90)
l2.grid(row=1,column=4,padx=90)

#teksta lauks rezultātu parādīšanai
results_text = tk.Text(root, wrap='word')
results_text.grid(row=5,column=1, padx=10, pady=10, columnspan=3)

#scrollbar pogas izveidošana
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=results_text.yview)
scrollbar.grid(row=5, column=4, sticky=tk.NS)
results_text.config(yscrollcommand=scrollbar.set)

dziesmasnos = tk.StringVar() #StringVar - kā strings
dziesmasnos.set("") #norāda sākotnējo vērtību

#izvelētās dziesmas saglabāšana
l3 = tk.Label(root,  text='Type in and save a song:', bg='lightblue')
l3.place(relx = 0.17, rely = 0.93, anchor ='sw')
choose_entry = tk.Entry(root, textvariable=dziesmasnos)
choose_entry.grid(row=6,column=1,padx=90)

def save(): #funkcija dziesmu saglabāšanai
    k1 = dziesmasnos.get()
    with open('DziesmasNosaukumi.txt', 'a') as f:
        f.write(k1 + '\n')


#saglabāšanas poga
save_button = tk.Button(root, text="Save", command=save)
save_button.grid(row=7,column=1,padx=90)

#start GUI
root.mainloop()
