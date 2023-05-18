import os
import platform
import time

import inquirer
import pyautogui
import pyKey as pk
from rich import print as rprint
from rich.progress import Progress, track
from rich.prompt import Prompt, IntPrompt, FloatPrompt

text_input = ""
version = "v1.1"

def init_input():
	input_type_prompt = [
		inquirer.List(
			"selected_input_type",
			message="Choose an input type",
			choices=[
				"Raw Text",
				"Text File"
			],
			carousel=True
		)
	]
	input_type = inquirer.prompt(input_type_prompt)
	rprint(f"📃 Current input type is set to [bold green]{input_type['selected_input_type']}[/bold green]")

	return input_type['selected_input_type']

def select_file():
	current_dir = os.getcwd()
	txt_files = []
	for file in os.listdir(current_dir):
		if file.endswith(".txt"):
			txt_files.append(file)

	text_file_prompt = [
		inquirer.List(
			"selected_file",
			message="Choose a text file",
			choices=txt_files,
			carousel=True
		)
	]
	text_file = inquirer.prompt(text_file_prompt)
	rprint(f"You chose [bold green]{text_file['selected_file']}[/bold green]")

	return text_file['selected_file']

def read_file(file_path):
	with open(file_path, 'r') as file:
		text = file.read()
	return text

def pykey_impl(key: str, interval: int | float):
	pk.press(key=key)
	time.sleep(interval)

def pyautogui_impl(key: str, interval: int | float):
	pyautogui.press(keys=key, interval=interval)

def main():
	os_type = platform.system()
	# Banner
	print(
""" _           _   ___ _               _           _
| |_ _____ _| |_|_  ) |_____ _  _ __| |_ _ _ ___| |_____ ___
|  _/ -_) \ /  _|/ /| / / -_) || (_-<  _| '_/ _ \ / / -_|_-<
 \__\___/_\_\\\__/___|_\_\___|\_, /__/\__|_| \___/_\_\___/__/
                             |__/
"""
	)
	rprint(f"Made by [blue]TrueMLGPro[/blue] | [bold green]{version}[/bold green]")
	input_type: str = init_input()

	if input_type == "Raw Text":
		text_input = Prompt.ask("💬 Enter the text to convert to keystrokes", default="hello world")
	elif input_type == "Text File":
		txt_file = select_file()
		text_input = read_file(txt_file)

	delay_before_input: int = IntPrompt.ask("⏳ Input an amount of seconds to wait before sending the keystrokes", default=5)
	delay_between_keystrokes: float = FloatPrompt.ask("⏲  Specify an interval (can be a floating point number) inbetween keystroke sends", default=0.01)

	# Splits text into a list of characters and replaces spaces with `SPACEBAR` or `space` key code depending on user's OS
	normalized_text_keystrokes = [
		keystroke.replace(" ", "SPACEBAR").replace("\n", "ENTER").replace("\r", "ENTER")
		if os_type == "Windows" or os_type == "Linux"
		else keystroke.replace(" ", "space").replace("\n", "enter").replace("\r", "enter")
		for keystroke in track(sequence=list(text_input), description="📝 Normalizing input...")
	]
	print("✅ Normalized input!")

	# Waits for specified amount of seconds before typing
	print(f"🕓 Waiting {delay_before_input} seconds before starting...")
	print("👆 Click on the window you want to type in")
	time.sleep(delay_before_input)

	# Displays progress for the operation
	with Progress() as progress:
		current_progress = 0
		task = progress.add_task("🤖 Typing...", total=len(normalized_text_keystrokes))
		for key in normalized_text_keystrokes:
			# Prints out current key position in the list
			current_progress += 1
			progress.console.print(f"Sending keystroke {current_progress} / {len(normalized_text_keystrokes)} - [bold blue]{key}[/bold blue]")
			# Checks OS to choose the implementation
			if os_type == "Windows" or os_type == "Linux":
				pykey_impl(key=key, interval=delay_between_keystrokes)
			elif os_type == "Darwin":
				pyautogui_impl(key=key, interval=delay_between_keystrokes)
			progress.advance(task)

	print("✅ Done!")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		rprint("\n⏹  [bold blue]Exiting...[/bold blue]")