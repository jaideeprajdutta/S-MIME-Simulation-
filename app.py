# app.py
import sys
sys.stdout.reconfigure(encoding='utf-8')
from flask import Flask, render_template, request, redirect, url_for
import subprocess, os

app = Flask(__name__)

def run_script(script_name):
    """Run one of the existing Python scripts and return output or error."""
    try:
        result = subprocess.run(
            ["python", script_name],
            capture_output=True,            
            text=True,
            encoding='utf-8'   # ensures emoji + unicode output works
        )

        if result.returncode == 0:
            return result.stdout or f"{script_name} executed successfully."
        else:
            return result.stderr or "An error occurred while running script."
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def index():
    """Main dashboard."""
    return render_template("index.html")

@app.route("/generate_keys")
def generate_keys():
    # Add debugging info
    current_dir = os.getcwd()
    keys_exist_before = os.path.exists("keys")
    
    message = run_script("generate_keys.py")
    
    # Check after running script
    keys_exist_after = os.path.exists("keys")
    key_files_after = []
    if keys_exist_after:
        key_files_after = os.listdir("keys")
    
    debug_info = f"""
Working Directory: {current_dir}
Keys folder existed before: {keys_exist_before}
Keys folder exists after: {keys_exist_after}
Key files after: {key_files_after}

Script Output:
{message}
"""
    
    return render_template("result.html", title="Generate RSA Keys", result=debug_info)

@app.route("/encrypt")
def encrypt():
    message = run_script("encrypt_email.py")
    return render_template("result.html", title="Encrypt & Sign Email", result=message)

@app.route("/decrypt")
def decrypt():
    message = run_script("decrypt_email.py")

    decrypted_path = "messages/email_decrypted.txt"
    decrypted_text = ""
    if os.path.exists(decrypted_path):
        with open(decrypted_path, "r", encoding="utf-8") as f:
            decrypted_text = f.read()

    return render_template("result.html", title="Decrypted Email", result=message, content=decrypted_text)

@app.route("/verify")
def verify():
    message = run_script("verify_signature.py")
    return render_template("result.html", title="Verify Signature", result=message)

@app.route("/view_keys")
def view_keys():
    """Display the contents of all key files."""
    keys_info = {}
    keys_dir = "keys"
    
    if os.path.exists(keys_dir):
        key_files = ["sender_private.pem", "sender_public.pem", "receiver_private.pem", "receiver_public.pem"]
        
        for key_file in key_files:
            key_path = os.path.join(keys_dir, key_file)
            if os.path.exists(key_path):
                try:
                    with open(key_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        keys_info[key_file] = {
                            "content": content,
                            "size": len(content),
                            "exists": True
                        }
                except Exception as e:
                    keys_info[key_file] = {
                        "content": f"Error reading file: {e}",
                        "size": 0,
                        "exists": False
                    }
            else:
                keys_info[key_file] = {
                    "content": "File not found",
                    "size": 0,
                    "exists": False
                }
    else:
        keys_info["error"] = "Keys directory not found"
    
    return render_template("keys.html", title="View RSA Keys", keys_info=keys_info)

if __name__ == "__main__":
    app.run(debug=True)
