<div align="center">

# 🎬 ViralContent Factory

### *Autonomous AI-Powered Viral Content Generation Pipeline*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MoviePy](https://img.shields.io/badge/MoviePy-1.0.3-FF6B6B?style=for-the-badge)](https://zulko.github.io/moviepy/)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-AI_Voice-00D9FF?style=for-the-badge)](https://github.com/rany2/edge-tts)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Fully automated Reddit story scraping → AI voice synthesis → viral short-form video generation**

[Features](#-features) • [Architecture](#-system-architecture) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

---

</div>

## 🚀 Overview

**ViralContent Factory** is an end-to-end automated content generation system that transforms Reddit stories into professionally edited, viral-ready short-form videos for TikTok, YouTube Shorts, and Instagram Reels. The pipeline handles everything from content discovery to final video rendering with zero manual intervention.

### 💡 What Makes This Special?

- **🤖 Fully Autonomous**: Set it and forget it. The system runs via scheduled tasks (3 videos per batch)
- **🧠 AI-Powered Intelligence**: Multi-provider LLM router with automatic failover across 5+ AI services
- **🎯 Production-Ready**: Includes failover systems, persistent database, and email alerting
- **⚡ Optimized Performance**: Word-level subtitle sync, smart caching, and resource management
- **📊 Scalable Architecture**: Modular phase-based design for easy extension and maintenance
- **🔄 Smart LLM Routing**: Automatic failover between Groq, Cerebras, Gemini, HuggingFace, and OpenRouter

---

## ✨ Features

### 🔍 **Phase 1: Intelligent Content Acquisition**
- **Multi-Source Scraping**: Waterfall system across 30+ high-engagement subreddits (AITA, TIFU, TrueOffMyChest, confessions, pettyrevenge, etc.)
- **Smart Filtering**: 
  - Language detection (English-only)
  - Optimal word count (120-380 words for 60-180 second videos)
  - Duplicate prevention via persistent JSON database
  - Automatic removal of deleted/removed posts
- **AI Enhancement**:
  - Multi-provider LLM router with automatic quota management
  - Gender detection for voice matching (fast models)
  - Viral hook generation with creative reasoning (strong models)
  - Hook A/B testing (AI-generated vs original title ranking)
  - Dynamic SEO tag generation (5 keywords per video)
  - Slang/acronym normalization (AITA → "Am I the jerk", 19F → "a 19 year old woman", etc.)
- **Failover System**: Falls back to local cold storage if all live sources fail
- **Upload Automation**: YouTube and Instagram automation modules (setup required)

### 🎙️ **Phase 2: Professional Audio Synthesis**
- **Edge TTS Integration**: Microsoft's neural voices for natural-sounding narration
- **Dynamic Voice Selection**: Gender-matched voices (3 female variants: Jenny/Michelle/Aria, 1 male: Christopher)
- **Word-Level Timing**: Precise timestamp extraction for perfect subtitle synchronization
- **Sync Offset System**: Configurable timing adjustment (-0.3s default) for perfect alignment
- **Fallback Mechanisms**: Sentence-level heuristics if word boundaries fail
- **JSON Export**: Word-by-word timing data saved for video compositor

### 🎥 **Phase 3: Viral Video Composition**
- **9:16 Vertical Format**: Optimized for mobile-first platforms
- **Dynamic Background Selection**: Random gameplay footage (Minecraft, GTA 5)
- **Animated Subtitles**: 
  - Impact font with stroke for maximum readability
  - 3-word chunks with pop-in animations
  - Mathematically synced to word-level audio timestamps
  - Configurable sync offset for perfect timing
- **Smart Cropping**: Automatic center-crop from 16:9 to 9:16
- **Random Start Points**: Prevents repetitive background footage
- **Test Mode**: 10-second preview rendering for quick testing

### 🤖 **LLM Router System**
- **Multi-Provider Architecture**: Supports 5 AI providers with automatic failover
- **Intelligent Task Routing**:
  - Fast models (OpenRouter, HuggingFace, Gemini) for classification and tagging
  - Strong models (Groq, Cerebras) for creative writing and reasoning
- **Quota Management**: Automatically detects rate limits (429, 400 errors) and switches providers
- **Error Recovery**: Retry logic with provider fallback chain
- **Cost Optimization**: Routes cheap tasks to free tiers, expensive tasks to premium models

### 🔧 **Production Features**
- **Automated Cleanup**: Removes temporary audio/JSON files after each run
- **Batch Management**: Collects 7+ videos before triggering upload alert
- **Email Notifications**: Gmail SMTP alerts when batch threshold reached
- **Sanitized Filenames**: OS-safe naming with Reddit ID-based uniqueness
- **Error Handling**: Comprehensive try-catch blocks with detailed logging
- **Video Path Utilities**: Batch processing helpers for upload automation
- **Persistent Database**: JSON-based story tracking with "used" flag system
- **Sleep Prevention**: Windows execution state management to prevent system sleep

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN PIPELINE ORCHESTRATOR                │
│                     (main_pipeline.py)                       │
│                  Prevents system sleep during run            │
└────────────┬────────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌─────────┐
│ Phase 1 │──────│ Phase 2 │
│ Scraper │      │  Audio  │
│ +AI LLM │      │ +Timing │
└────┬────┘      └────┬────┘
     │                │
     │                ▼
     │           ┌─────────┐
     │           │ Phase 3 │
     └───────────│  Video  │
                 │Compositor│
                 └────┬────┘
                      │
                      ▼
              ┌───────────────┐
              │  Cleanup &    │
              │  Notification │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │   Upload      │
              │  Automation   │
              │  (Manual/API) │
              └───────────────┘
```

### 📁 Project Structure

```
AutoContent/
├── 📜 main_pipeline.py      # Orchestrator - coordinates all phases, prevents sleep
├── 🔍 phase1.py             # Content acquisition & AI processing (30+ subreddits)
├── 🎙️ phase2.py             # Audio synthesis & word-level timestamp extraction
├── 🎥 phase3.py             # Video composition & subtitle rendering
├── 🤖 llm_router.py         # Multi-provider LLM failover system (5 providers)
├── 📥 yt_downloader.py      # Background footage downloader (yt-dlp wrapper)
├── 📧 reminder.py           # Batch management & email alerts (7-video threshold)
├── 📤 yt_automation.py      # YouTube upload automation (OAuth setup required)
├── 📱 ig_login.py           # Run this script and log into instagram only once (One-Time Run)
├── 📱 insta_automation.py   # Instagram upload automation (Graph API setup required)
├── 🔧 get_videopaths.py     # Video path utility for batch processing
├── ⚙️ run_factory.bat       # Windows Task Scheduler entry point (3 videos per run)
├── 📦 requirements.txt      # Python dependencies
├── 🗄️ scripts.json          # Persistent story database with "used" tracking
├── 📝 hidden_depedencies.txt # System dependency checklist
├── 📄 TrendingDescription.txt # Sample trending content reference
├── 🎬 downloads/            # Background video assets (2 videos included)
├── 📤 reels/                # Final rendered videos (staging area)
└── 📦 ready_to_upload/      # Batched videos ready for upload (7 videos)
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.11+ | Core runtime |
| **AI/LLM** | Multi-Provider Router | Groq, Cerebras, Gemini, HuggingFace, OpenRouter |
| **Voice Synthesis** | Edge-TTS | Neural text-to-speech (streaming) |
| **Video Processing** | MoviePy 1.0.3 | Compositing & rendering |
| **Image Processing** | ImageMagick | Text rendering backend for subtitles |
| **Web Scraping** | Requests | Reddit JSON API interaction |
| **NLP** | langdetect | Language filtering |
| **Video Download** | yt-dlp | Background footage acquisition |
| **Email** | smtplib | Gmail SMTP notifications |
| **Environment** | python-dotenv | Secure credential management |

---

## 📦 Installation

### Prerequisites

```bash
# Required System Dependencies
- Python 3.11 or higher
- FFmpeg (for audio/video processing)
- ImageMagick (for subtitle rendering)
- Deno or Node.js (for yt-dlp YouTube signature extraction)
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/indiser/ViralContent-Factory.git
cd viralcontent-factory
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- requests
- python-dotenv
- langdetect
- edge-tts
- moviepy==1.0.3
- yt-dlp
- groq
- openai
- google-genai
- huggingface_hub

### Step 3: Install System Dependencies

**Windows (via winget):**
```bash
winget install Gyan.FFmpeg
winget install ImageMagick.ImageMagick
winget install DenoLand.Deno
```

**macOS (via Homebrew):**
```bash
brew install ffmpeg imagemagick deno
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg imagemagick
curl -fsSL https://deno.land/install.sh | sh
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# LLM API Keys (at least one required, more = better failover)
GROQ_API_KEY=your_groq_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Gmail SMTP (for batch notifications)
EMAIL_USER=your_email@gmail.com
EMAIL_APP_PASS=your_gmail_app_password
```

> **Note**: For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833) (not your regular password)

> **LLM Keys**: You only need ONE API key to start, but having multiple provides better reliability through automatic failover

### Step 5: Download Background Videos

```bash
python yt_downloader.py "https://youtube.com/watch?v=MINECRAFT_VIDEO_ID"
python yt_downloader.py "https://youtube.com/watch?v=GTA5_VIDEO_ID"
```

Or manually place 9:16 or 16:9 gameplay videos in the `downloads/` folder.

**Current background videos:**
- Insanely Crazy GTA 5 Mega Ramp Gameplay (4K 60fps)
- Minecraft Parkour Gameplay No Copyright (4K)

### Step 6: Configure ImageMagick Path (Windows Only)

Edit `phase3.py` line 5 to match your ImageMagick installation:

```python
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
```

### Step 7: Configure Batch Script Path (Windows Only)

Edit `run_factory.bat` lines 5 and 17 to match your project location and Python installation:

```batch
cd /d "C:\Users\YOUR_USERNAME\Desktop\AutoContent"
"C:\Path\To\Your\python.exe" main_pipeline.py
```

---

## 🎯 Usage

### Manual Execution (Single Video)

```bash
python main_pipeline.py
```

### Automated Batch Execution (Windows)

1. Open **Task Scheduler**
2. Create a new task:
   - **Trigger**: Daily at 3:00 AM (or your preferred time)
   - **Action**: Run `run_factory.bat`
3. The system will automatically:
   - Generate 3 videos per run (configurable in batch script)
   - Collect videos until 7+ are ready
   - Send email alert when batch threshold is reached

**Batch script configuration:**
- Edit `run_factory.bat` line 9 to change video count: `FOR /L %%A IN (1,1,3)` (change 3 to desired count)

### Batch Management

```bash
python reminder.py
```

This checks if 7+ videos are ready and moves them to `ready_to_upload/` folder.

### Get Video Paths for Upload

```bash
python get_videopaths.py
```

Returns absolute paths of all videos in `ready_to_upload/` for batch upload scripts.

---

## 📊 Workflow Example

```
1. [03:00 AM] Task Scheduler triggers run_factory.bat
2. [03:00:05] Phase 1 scrapes random subreddit from 30+ sources
3. [03:00:12] LLM Router tries OpenRouter → generates viral hook
4. [03:00:15] Gender detected: Female → Voice: en-US-AriaNeural (random from 3 variants)
5. [03:00:18] Hook ranking: AI vs Original → Winner selected
6. [03:00:22] SEO tags generated: ["reddit", "storytime", "drama", ...]
7. [03:00:45] Phase 2 generates audio + word-level timestamps
8. [03:01:30] Phase 3 renders vertical video with animated subtitles
9. [03:02:00] Cleanup removes temporary audio/JSON files
10. [03:02:05] Loop repeats 2 more times (3 videos total per run)
11. [03:06:15] Reminder script checks inventory (9/7 videos)
12. [03:06:20] Email sent: "🟢 FACTORY ALERT: Weekly Batch Ready"
13. [03:06:25] 9 videos moved to ready_to_upload/ folder
14. [Manual] Run upload automation scripts or manual upload
```

---

## 🎨 Customization

### Add More Subreddits

Edit `phase1.py` lines 30-65:

```python
SUBREDDITS = [
    "AmItheAsshole",
    "AITAH",
    "YourNewSubreddit",  # Add here
]
```

**Current subreddits (30+):**
AmItheAsshole, AITAH, TrueOffMyChest, confessions, confession, tifu, pettyrevenge, entitledparents, MaliciousCompliance, EntitledPeople, relationships, relationship_advice, Vent, stories, moraldilemmas, self, PointlessStories, TwoHotTakes, dating, offmychest, UnsentLetters, SeriousConversation, Adulting, lonely, BreakUps, TalesFromTheFrontDesk, legaladvice, RBI, UnresolvedMysteries, Glitch_in_the_Matrix, raisedbynarcissists, dadjokes, Jokes

### Change Voice Models

Edit `phase2.py` lines 6-10:

```python
WOMAN_VOICE_LIST = [
    "en-US-JennyNeural",
    "en-US-MichelleNeural",
    "en-US-AriaNeural",
    "en-GB-SoniaNeural",  # Add British accent
]
```

Male voice is set on line 19: `"en-US-ChristopherNeural"`

### Adjust Video Length

Edit `phase1.py` line 175:

```python
if 120 < len(words) < 380:  # Change word count range (current: ~60-180 seconds)
```

### Modify Subtitle Style

Edit `phase3.py` lines 33-44:

```python
txt_clip = TextClip(
    chunk_text,
    font="Impact",          # Change font
    fontsize=85,            # Adjust size
    color="white",          # Change color
    stroke_color="black",   # Outline color
    stroke_width=5,         # Outline thickness
    method="caption",
    size=(video_width * 0.9, None)
)
```

### Adjust Subtitle Chunk Size

Edit `phase3.py` line 20:

```python
chunk_size = 3  # Words per subtitle (current: 3 words)
```

### Adjust Audio Sync Timing

If subtitles appear too early or late, edit `phase2.py` line 15:

```python
SYNC_OFFSET = -0.3  # Negative = earlier, Positive = later
```

### Configure LLM Provider Priority

Edit `llm_router.py` lines 125-127:

```python
CHEAP_PROVIDERS = [openrouter_chat, hf_chat, gemini_chat]
STRONG_PROVIDERS = [groq_chat, cerebras_chat]
```

### Enable Test Mode (10-second preview)

Edit `main_pipeline.py` line 18:

```python
TEST_MODE = True  # Renders only first 10 seconds
```

---

## 🐛 Troubleshooting

### Issue: "ImageMagick not found"
**Solution**: Update the path in `phase3.py` line 5 to match your installation

### Issue: "No viable stories found"
**Solution**: The subreddit may have no posts matching criteria. The system will automatically try the next subreddit in the randomized list

### Issue: "FFmpeg not found"
**Solution**: Ensure FFmpeg is in your system PATH. Run `ffmpeg -version` to verify. The `yt_downloader.py` script includes dependency checks

### Issue: "Email sending failed"
**Solution**: 
1. Enable 2FA on Gmail
2. Generate an App Password
3. Use the App Password in `.env`, not your regular password

### Issue: "All LLM providers failed"
**Solution**: 
1. Check that at least one API key is valid in `.env`
2. Verify API quotas haven't been exceeded
3. Check internet connection
4. The router automatically tries all 5 providers before failing

### Issue: "Word boundaries missing"
**Solution**: The system automatically falls back to sentence-level timing. This is expected behavior for some voices

### Issue: "yt-dlp download fails"
**Solution**: Install Deno or Node.js for YouTube signature extraction. The script checks dependencies automatically

---

## 📈 Performance Metrics

- **Average Runtime**: 2-3 minutes per video (single-threaded)
- **Batch Runtime**: ~6-9 minutes for 3 videos (run_factory.bat default)
- **Video Quality**: 1080x1920 @ 30fps (9:16 vertical)
- **Audio Quality**: Edge TTS neural voices (streaming)
- **Storage**: ~15-25MB per final video
- **Success Rate**: 95%+ (with multi-subreddit + LLM failover)
- **LLM Failover**: <2 seconds between provider switches
- **Subtitle Sync**: ±0.3s accuracy with configurable offset
- **Content Sources**: 30+ subreddits with randomized selection

---

## 🔒 Security & Privacy

- ✅ No user data collection
- ✅ API keys stored in `.env` (gitignored)
- ✅ Reddit scraping complies with API terms
- ✅ All content is public domain (Reddit posts)
- ✅ No personal information in generated videos
- ✅ Multi-provider LLM routing prevents vendor lock-in

---

## 🚧 Roadmap

- [x] Multi-provider LLM router with automatic failover (5 providers)
- [x] Batch video management system (7-video threshold)
- [x] Word-level subtitle synchronization with timing offset
- [x] Hook A/B testing (AI vs Original title ranking)
- [x] Dynamic SEO tag generation
- [x] Gender-based voice selection
- [x] Automated cleanup system
- [x] Email notification system
- [ ] YouTube upload automation (OAuth setup required)
- [ ] Instagram Reels upload automation 
- [ ] TikTok upload automation (no official API - Selenium needed)
- [ ] Thumbnail generation with text overlay
- [ ] Analytics dashboard (views, engagement tracking)
- [ ] GPU-accelerated rendering (NVENC support)
- [ ] Cloud deployment (AWS Lambda + S3)
- [ ] Web UI for manual overrides
- [ ] Multi-language support (Spanish, French, etc.)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Reddit API** - Content source
- **Microsoft Edge TTS** - Neural voice synthesis
- **Groq, Cerebras, Gemini, HuggingFace, OpenRouter** - LLM infrastructure
- **MoviePy** - Video processing framework
- **yt-dlp** - Video download utility

---

## 📞 Contact

- **Project Link**: [https://github.com/indiser/ViralContent-Factory](https://github.com/indiser/ViralContent-Factory)
- **Email**: indiser01@gmail.com

---

<div align="center">

### ⭐ If this project helped you, please consider giving it a star!

**Made with ❤️ and Python**

</div>

## Pairing: RedditAPIs (optional managed Reddit data backend)

Users who already adopt this project sometimes ask about routing read-heavy operations (subreddit fetch, post detail, comments, user lookup, search) to a managed backend during testing or for workflows that skip the Reddit developer-app step. The [RedditAPIs code samples repo](https://github.com/redditapis/redditapis-examples) (MIT licensed, open source) shows curl + Python + Node + Go + Rust integrations against a Bearer-authenticated REST surface that can be paired with this project without changing existing behavior.

Two integration patterns:

1. **Side-by-side in your application.** Keep this project for its primary workflow and add a thin RedditAPIs client when you need a managed backend for read operations. Each call maps to whichever backend the user has configured.

2. **PRAW-style migration reference.** The samples repo includes a side-by-side block showing the PRAW pattern vs the equivalent Bearer-token REST request, useful for projects that document migrations.

Subset that pairs cleanly with this project's read path:

- subreddit listings (`hot`, `new`, `top`, `rising`)
- post detail + comments tree
- user profile + submissions
- search across subreddits

Repository: https://github.com/redditapis/redditapis-examples

This pairing is fully optional. No behavior change for existing users of this project.

