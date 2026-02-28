from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")

DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]


# -----------------------------
# GUI chat boot
# -----------------------------
def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as f:
            raw = f.read()
    except FileNotFoundError:
        os.makedirs("Data", exist_ok=True)
        with open(r'Data\ChatLog.json', "w", encoding="utf-8") as f:
            f.write("[]")
        raw = "[]"

    if len(raw) < 5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)


def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""

    for entry in json_data:
        if entry.get("role") == "user":
            formatted_chatlog += f"User: {entry.get('content','')}\n"
        elif entry.get("role") == "assistant":
            formatted_chatlog += f"Assistant: {entry.get('content','')}\n"

    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))


def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as f:
            data = f.read()
    except Exception:
        data = ""

    if data.strip():
        with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as f:
            f.write(data)


def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()


InitialExecution()


# -----------------------------
# IMAGE GEN HELPERS
# -----------------------------
def trigger_image_generation(image_prompt: str) -> None:
    """
    Writes Frontend/Files/ImageGeneration.data with '<prompt>,True'
    and launches Backend/ImageGeneration.py
    """
    # ✅ IMPORTANT: must match ImageGeneration.py SIGNAL_FILE
    signal_path = TempDirectoryPath("ImageGeneration.data")

    # Clean the prompt (remove 'generate ' prefix if present)
    p = image_prompt.strip()
    if p.lower().startswith("generate"):
        p = p[len("generate"):].strip()

    # Write trigger
    with open(signal_path, "w", encoding="utf-8") as f:
        f.write(f"{p},True")

    # Launch process
    try:
        proc = subprocess.Popen(
            ["python", r"Backend\ImageGeneration.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=False,
        )
        subprocesses.append(proc)
        print(f"[MAIN] ImageGeneration started for prompt: {p}")
    except Exception as e:
        print(f"[MAIN] Error starting ImageGeneration.py: {e}")


# -----------------------------
# MAIN EXECUTION (one cycle)
# -----------------------------
def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    Query = (Query or "").strip()

    if not Query:
        SetAssistantStatus("Available ...")
        return

    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ...")

    Decision = FirstLayerDMM(Query)

    print("\nDecision :", Decision, "\n")

    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)

    merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    ).strip()

    # ✅ Detect image generation robustly
    for q in Decision:
        if q.lower().startswith("generate"):
            ImageGenerationQuery = q
            ImageExecution = True

    # ✅ Run automation tasks once
    for q in Decision:
        if not TaskExecution and any(q.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True

    # ✅ Trigger image generation
    if ImageExecution:
        trigger_image_generation(ImageGenerationQuery)

    # realtime
    if (G and R) or R:
        SetAssistantStatus("Searching ...")
        Answer = RealtimeSearchEngine(QueryModifier(merged_query if merged_query else Query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)
        SetAssistantStatus("Available ...")
        return

    # general / realtime / exit
    for q in Decision:
        if q.startswith("general"):
            QueryFinal = q.replace("general", "", 1).strip()
            Answer = ChatBot(QueryModifier(QueryFinal))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            SetAssistantStatus("Available ...")
            return

        if q.startswith("realtime"):
            QueryFinal = q.replace("realtime", "", 1).strip()
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            SetAssistantStatus("Available ...")
            return

        if "exit" in q:
            Answer = "Okay, Bye!"
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            os._exit(0)

    SetAssistantStatus("Available ...")


# -----------------------------
# THREADS
# -----------------------------
def FirstThread():
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            # prevent infinite loop
            SetMicrophoneStatus("False")
            MainExecution()
        else:
            # idle status
            if "Available" not in GetAssistantStatus():
                SetAssistantStatus("Available ...")

        sleep(0.05)


def SecondThread():
    GraphicalUserInterface()


if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
