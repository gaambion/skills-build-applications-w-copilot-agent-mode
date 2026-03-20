# OctoFit Tracker API Testing Guide

## ✅ Codespace Configuration Status

Your Django backend is now fully configured for codespace deployment:

### 1. **ALLOWED_HOSTS Configuration** ✓
File: [octofit-tracker/backend/octofit_tracker/settings.py](octofit-tracker/backend/octofit_tracker/settings.py)

```python
import os
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if os.environ.get('CODESPACE_NAME'):
    ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")
```

✅ Supports both:
- `localhost:8000` (local development)
- `https://$CODESPACE_NAME-8000.app.github.dev` (GitHub Codespace)

### 2. **URLs Configuration** ✓
File: [octofit-tracker/backend/octofit_tracker/urls.py](octofit-tracker/backend/octofit_tracker/urls.py)

```python
import os
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"
```

✅ REST API Endpoints:
- `/api/users/` - User management
- `/api/teams/` - Team management  
- `/api/activities/` - Activity logging
- `/api/leaderboard/` - Competitive leaderboard
- `/api/workouts/` - Workout suggestions

### 3. **Launch Configuration** ✓
File: [.vscode/launch.json](.vscode/launch.json)

Configured to start Django backend on `0.0.0.0:8000` with proper Python virtual environment.

---

## 🚀 How to Start the Server

### Option 1: Using VS Code Launch (Recommended)
1. Open the Debug View in VS Code (Ctrl+Shift+D / Cmd+Shift+D)
2. Select "**Launch Django Backend**" from dropdown
3. Click the green play button to start
4. Server will start on `0.0.0.0:8000`

### Option 2: Manual Command Line
```bash
cd octofit-tracker/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

---

## 🧪 Testing API Endpoints

### Test 1: API Root Endpoint
```bash
# Via localhost
curl http://localhost:8000/api/

# Via codespace (when deployed)
curl https://$CODESPACE_NAME-8000.app.github.dev/api/
```

Expected Response:
```json
{
  "users": "/api/users/",
  "teams": "/api/teams/",
  "activities": "/api/activities/",
  "leaderboard": "/api/leaderboard/",
  "workouts": "/api/workouts/"
}
```

### Test 2: List All Users
```bash
curl -X GET http://localhost:8000/api/users/
```

### Test 3: Create a New User
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

### Test 4: List All Teams
```bash
curl -X GET http://localhost:8000/api/teams/
```

### Test 5: List All Activities
```bash
curl -X GET http://localhost:8000/api/activities/
```

### Test 6: Get Leaderboard
```bash
curl -X GET http://localhost:8000/api/leaderboard/
```

### Test 7: Get Workout Suggestions
```bash
curl -X GET http://localhost:8000/api/workouts/
```

### Test with Pretty JSON Output
Add `-s | python -m json.tool` to prettify responses:
```bash
curl -s http://localhost:8000/api/ | python -m json.tool
```

### Check Server with Verbose Output
```bash
curl -v http://localhost:8000/api/
```

---

## 🔍 Debugging Tips

### View Django server logs
- Server logs appear in the integrated terminal when running via VS Code Launch
- Look for HTTP requests and any errors

### Test Codespace Domain (when running in GitHub Codespace)
```bash
# First, check if CODESPACE_NAME is set
echo $CODESPACE_NAME

# Test via codespace domain
curl https://$CODESPACE_NAME-8000.app.github.dev/api/
```

### CORS Issues
- CORS is already enabled for all origins in settings.py
- If you get CORS errors, check that port 8000 is public (it is by default)

### Port Forwarding
- Port 8000 is already forwarded as public in devcontainer
- Port 3000 (frontend) is also forwarded as public
- MongoDB port 27017 is private (local dev only)

---

## 📝 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/` | GET | API root with all available endpoints |
| `/api/users/` | GET, POST | List users or create new user |
| `/api/users/{id}/` | GET, PUT, DELETE | User operations |
| `/api/teams/` | GET, POST | List teams or create new team |
| `/api/teams/{id}/` | GET, PUT, DELETE | Team operations |
| `/api/activities/` | GET, POST | List activities or log new activity |
| `/api/activities/{id}/` | GET, PUT, DELETE | Activity operations |
| `/api/leaderboard/` | GET | View competitive leaderboard |
| `/api/workouts/` | GET | Get personalized workout suggestions |

---

## ✅ Configuration Checklist

- [x] `settings.py` - ALLOWED_HOSTS configured with environment variable
- [x] `urls.py` - Base URL configured with environment variable  
- [x] `launch.json` - Django backend launcher configured
- [x] Virtual environment - Python venv ready in `octofit-tracker/backend/venv/`
- [x] Requirements - All packages installed from requirements.txt
- [x] Database - MongoDB configured (djongo ORM)
- [x] CORS - Enabled for frontend communication
- [x] REST Framework - Configured with routers and viewsets

Your API is ready to test! 🎉
