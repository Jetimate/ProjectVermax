import json

from pathlib import Path
import json

BASE_DIR = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory.json"

def setup():
    print("Vermax: talk to me, I'm listening:>")


def loop():
    userInput = input()

    # Read existing memory
    with open(MEMORY_FILE, "r") as file:
        memory = json.load(file)

    found = False
    for intention in memory:
        for operator in memory["math"]["examples"]:
            if operator in userInput:
                found = True
                print(f"Vermax: Your text has a {operator} operator. Do you want me to calculate?")
                userResponse = input()
                if userResponse in memory["agreement"]["examples"]:
                    print("so you agree then")
                elif userResponse in memory["disagreement"]["examples"]:
                    print("so you disagree then")
                break

        if found:
            break
        elif userInput in memory[intention]["examples"]:
            found = True
            response = memory[intention]["responses"]
            if response:
                print(f"Vermax: {response[0]}")
                break
            else:
                print(f"Vermax: Yes, you said that earlier, but how should I reply to that?")
                memory[intention]["responses"].append(input())
                print(f"Vermax: Alright")
                break

    if not found:
        # Add new message to memory
        if userInput in memory["disregard"]["examples"]:
            print(f"Vermax: {memory["disregard"]["responses"][0]}")
        elif "?" in userInput:
            print("Vermax: idk how to reply to that, sorry ._.")
            memory["question"]["examples"].append(userInput)
        else:
            print(f"Vermax: what is {userInput}?")
            intention = input()

            if intention in memory["disregard"]["examples"]:
                print(f"Vermax: {memory["disregard"]["responses"][0]}")
            else:
                if intention in memory:
                    memory[intention]["examples"].append(userInput)
                else:
                    memory[intention] = {"examples": {}, "responses": {}}
                    memory[intention]["examples"].append(userInput)

                print(f"Vermax: oki, {userInput} is {intention}")

    # Save to memory
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)
        

# code runs here
setup()

# makes the loop run forever ;-;
while True:
    loop()