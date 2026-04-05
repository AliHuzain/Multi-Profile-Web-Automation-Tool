import os
import customtkinter as ctk
from playwright.sync_api import sync_playwright, Error as PlaywrightError
from pynput import keyboard

# ================== CONFIG ==================
TARGET_URL = "https://your-site.com"
BUTTON_TEXT = "Any Button you want"
CLICK_INTERVAL = 65.0
# ============================================

profiles_dir = os.path.join(os.getcwd(), "profiles")
os.makedirs(profiles_dir, exist_ok=True)

profiles = {}
playwright_instance = None
browser_instance = None


def profile_state_path(profile_name):
    safe = profile_name.replace(" ", "_")
    folder = os.path.join(profiles_dir, safe)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "state.json")


def log(profile_name, message):
    try:
        log_text.configure(state="normal")
        log_text.insert("end", f"[{profile_name}] {message}\n")
        log_text.see("end")
        log_text.configure(state="disabled")
    except:
        pass


def update_profile_color(profile):
    profile["frame"].configure(
        fg_color="#1f6d1f" if profile.get("running") else "#444444"
    )


def update_status():
    active = [p for p in profiles.values() if p.get("running")]
    status_label.configure(text=f"Running Profiles: {len(active)}")


def start_hotkey_listener():
    def on_press(key):
        if key == keyboard.Key.f8:
            for prof in profiles.values():
                prof["running"] = not prof.get("running", False)
                update_profile_color(prof)
            update_status()

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


def create_context(profile_name):
    st_path = profile_state_path(profile_name)

    if os.path.exists(st_path):
        ctx = browser_instance.new_context(storage_state=st_path)
        log(profile_name, "Loaded saved session")
    else:
        ctx = browser_instance.new_context()
        log(profile_name, "New session")

    return ctx


def open_profile(profile_name):
    profile = profiles.get(profile_name)
    if not profile:
        return

    if "page" in profile:
        profile["running"] = True
        update_profile_color(profile)
        update_status()
        schedule_task(profile_name)
        return

    ctx = create_context(profile_name)
    profile["context"] = ctx
    page = ctx.new_page()
    profile["page"] = page

    page.goto(TARGET_URL, wait_until="domcontentloaded")
    log(profile_name, f"Opened {TARGET_URL}")

    profile["running"] = True
    update_profile_color(profile)
    update_status()

    schedule_task(profile_name)


def schedule_task(profile_name):
    root.after(0, lambda: run_task(profile_name))


def run_task(profile_name):
    profile = profiles.get(profile_name)

    if not profile or not profile.get("running") or "page" not in profile:
        root.after(1000, lambda: run_task(profile_name))
        return

    try:
        button = profile["page"].locator(f"text='{BUTTON_TEXT}'")

        if button.count() > 0:
            button.first.click()
            log(profile_name, f"Clicked '{BUTTON_TEXT}'")

            profile["context"].storage_state(
                path=profile_state_path(profile_name)
            )
        else:
            log(profile_name, f"Button '{BUTTON_TEXT}' not found")

    except PlaywrightError as e:
        log(profile_name, f"Error: {e}")

    root.after(int(CLICK_INTERVAL * 1000), lambda: run_task(profile_name))


def add_profile():
    profile_name = f"Profile {len(profiles)+1}"

    frame = ctk.CTkFrame(profiles_container, corner_radius=8, fg_color="#444444")
    frame.pack(fill="x", pady=5, padx=10)

    label = ctk.CTkLabel(frame, text=profile_name)
    label.pack(side="left", pady=8, padx=8)

    run_btn = ctk.CTkButton(
        frame,
        text="Run",
        width=70,
        command=lambda: open_profile(profile_name),
    )
    run_btn.pack(side="right", padx=8)

    profiles[profile_name] = {
        "frame": frame,
        "label": label,
        "running": False,
    }


def close_all():
    for profile in profiles.values():
        try:
            if "page" in profile:
                profile["page"].close()
            if "context" in profile:
                profile["context"].close()
        except:
            pass


# ================== INIT ==================
playwright_instance = sync_playwright().start()
browser_instance = playwright_instance.chromium.launch(headless=False)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Multi Profile Web Automation Tool")
root.geometry("700x800")

status_label = ctk.CTkLabel(root, text="Running Profiles: 0", font=("Arial", 16))
status_label.pack(pady=10)

profiles_scroll = ctk.CTkScrollableFrame(root)
profiles_scroll.pack(fill="both", expand=True, padx=10, pady=10)

profiles_container = ctk.CTkFrame(profiles_scroll)
profiles_container.pack(fill="both", expand=True)

log_frame = ctk.CTkFrame(root)
log_frame.pack(fill="both", padx=10, pady=10)

log_text = ctk.CTkTextbox(log_frame, height=250)
log_text.pack(fill="both", expand=True)
log_text.configure(state="disabled")

bottom = ctk.CTkFrame(root)
bottom.pack(fill="x", padx=10, pady=10)

ctk.CTkButton(bottom, text="Add Profile", command=add_profile).pack(
    side="left", padx=6
)

start_hotkey_listener()

# Clean exit
def on_close():
    close_all()
    browser_instance.close()
    playwright_instance.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
