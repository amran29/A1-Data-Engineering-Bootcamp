---

### 2. Frontend README
**File Path:** `investment_app/README.md`

```markdown
# 📱 Investment Portfolio Tracker - Flutter App

A modern, cross-platform mobile application that provides investors with a real-time view of their financial holdings. Designed for high performance and a premium user experience.

**Developer:** Amran Al-gaafari

## 🎨 UI/UX Highlights
- **Real-time Monitoring**: Track gains and losses with a clean, intuitive dashboard.
- **Portfolio Distribution**: Visual representation of asset allocation.
- **Secure Access**: Persistent login sessions using encrypted local storage for JWT tokens.
- **Responsive Design**: Optimized for both Android and iOS devices.

## 🛠 Tech Stack
- **Flutter & Dart**: UI toolkit for building natively compiled applications.
- **Dio**: Powerful HTTP client for interacting with the FastAPI backend.
- **Provider / Riverpod**: For efficient state management across the app.
- **JSON Serializable**: For automated data parsing between Python and Dart.

## 📂 Architecture (Clean Code Approach)
- `lib/core/`: Application constants, API client configurations, and themes.
- `lib/models/`: Data classes for Users and Assets.
- `lib/services/`: The logic layer responsible for API communication.
- `lib/views/`:
- `auth/`: Login and Signup screens.
- `portfolio/`: Dashboard, asset list, and management screens.

## ⚙️ Setup & Installation
1. **Prerequisites**: Ensure Flutter SDK is installed.
2. **Install Packages:**
```bash
flutter pub get