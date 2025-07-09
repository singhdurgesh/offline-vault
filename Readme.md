# Offline Vault

Offline Vault is a privacy-first, deterministic password manager that allows users to generate strong, policy-driven passwords based on a master secret and service identifier — all without ever storing passwords. Designed for offline-first use, it also supports optional encrypted backups to Google Cloud or offline storage.

----
## How to Run Locally

**Step 1:** Clone the repository  
```sh
git clone https://github.com/singhdurgesh/offline-vault.git
cd offline-vault
```

**Step 2:** Copy the sample config file  
```sh
cp config.json.sample config.json
```

**Step 3:** (Optional) Update `config.json` with your desired settings.

**Step 4:** Create a master key — a memorable string known only to you (e.g., "Hello World").

**Step 5:** Run the script  
```sh
python password_manager.py
```

**Step 6:** Enter your master key when prompted and press Enter.

**Step 7:** Passwords will be generated according to your configuration.

⸻

🚀 Current Status
- ✅ Core algorithm is implemented in Python
- ✅ Supports password generation with constraints:
- Character requirements (uppercase, lowercase, digits, specials)
- Password length
- Rotation policies (second, minute, hour, day, week, month)
- ✅ Cryptographically deterministic output using SHA-256 + shuffle logic

⸻

## 📌 Planned Features / Next Steps

#### 1. 🔁 Multi-Language Library Support

Implement core logic in:
- Python ✅ (done)
- Go
- Rust
- JavaScript/TypeScript
- Java/Kotlin (Android SDK)

#### 2. 📜 RFC Publication
- Define an RFC for deterministic password generation
- Include rotation mechanics, hash inputs, constraints
- Publish RFC as a technical whitepaper and open for review

#### 3. 📱 App Development
- Android/iOS app (Flutter/React Native)
- Allow local key storage encrypted using user passphrase
- Display, copy, export passwords

#### 4. ☁️ Backup & Sync (Optional)
- Store encrypted vault backup to Google Cloud
- Allow exporting encrypted JSON for offline backup
- Add secure import/export pipeline

⸻

💡 Why Offline Vault?
- ✨ Fully deterministic: No need to store passwords
- 🔒 Secure: Based on SHA-256, with strict character constraints
- 💾 Offline-first: Zero cloud dependence by default
- ☁️ Backup-friendly: Optional, encrypted cloud/offline backups
- 🛠️ Configurable: Rotate by time, enforce character rules

⸻

## 📂 Folder Structure (planned)

```
offline-vault/
├── libs/                   # Language-specific libraries
├── cli/                    # CLI version of the vault
├── app/                    # GUI app version
├── config.json             # Sample configuration
├── password_manager.py     # Core generator logic
├── password_config_model.py
├── README.md
```


⸻

## 🙋‍♂️ Contributing

Want to contribute? Open an issue or submit a PR!

⸻

## 📄 License

MIT License – use, modify, distribute freely.