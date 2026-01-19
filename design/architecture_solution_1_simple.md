# Architecture Solution 1: Simple MVP Architecture

## Overview

This solution prioritizes **simplicity and speed of development**. It's designed for a single developer to build quickly, perfect for prototyping and validating the game concept with your 5-year-old.

**Best For**: MVP/Prototype, single-player, local deployment, family use

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Vanilla JavaScript + HTML5                  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│  │
│  │  │  Game UI    │  │ Chess Board │  │  Train Station Builder  ││  │
│  │  │  (HTML/CSS) │  │ (Canvas)    │  │  (Canvas/SVG)           ││  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘│  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │              Local Storage (Backup Save)                │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/REST
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SERVER (Python Flask)                        │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                      Flask Application                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│  │
│  │  │   Routes    │  │   Puzzles   │  │    Game Logic           ││  │
│  │  │   (API)     │  │   (JSON)    │  │    (Python)             ││  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘│  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                    │                                 │
│                                    ▼                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                  MySQL (Single Database)                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│  │
│  │  │   Users     │  │  Progress   │  │     Game State          ││  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────┘│  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
| Component | Technology | Why |
|-----------|------------|-----|
| Framework | Vanilla JavaScript | No build step, simple deployment |
| Chess Logic | chess.js | Well-tested library for chess rules |
| UI Framework | None (pure HTML/CSS) | Maximum simplicity |
| Board Rendering | HTML5 Canvas | Simple drawing, good performance |
| Animations | CSS Animations + requestAnimationFrame | Native, no dependencies |
| Local Storage | Browser localStorage | Backup saves, offline capability |

### Backend
| Component | Technology | Why |
|-----------|------------|-----|
| Framework | Flask 3.0 | Simple, minimal, Python-native |
| Database ORM | SQLAlchemy | Easy MySQL integration |
| Chess Validation | python-chess | Server-side puzzle validation |
| Static Files | Flask built-in | Serves frontend directly |
| CORS | Flask-CORS | Simple cross-origin support |

### Database
| Component | Technology | Why |
|-----------|------------|-----|
| Database | MySQL 8.0 | As specified, reliable |
| Connection | PyMySQL | Pure Python MySQL driver |

### Development Tools
| Tool | Purpose |
|------|---------|
| pip | Python package management |
| venv | Python virtual environment |
| Live Server | Local development (VS Code extension) |

---

## Database Schema

```sql
-- Core user management
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    is_child BOOLEAN DEFAULT TRUE,
    parent_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE SET NULL
);

-- User preferences and settings
CREATE TABLE user_settings (
    user_id INT PRIMARY KEY,
    sound_enabled BOOLEAN DEFAULT TRUE,
    music_enabled BOOLEAN DEFAULT TRUE,
    hint_mode ENUM('always', 'limited', 'earned') DEFAULT 'always',
    daily_time_limit_minutes INT NULL,
    theme VARCHAR(20) DEFAULT 'default',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Static puzzle definitions (loaded from JSON at startup)
CREATE TABLE puzzles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    module VARCHAR(50) NOT NULL,           -- 'pawn_power', 'rook_railways', etc.
    collection VARCHAR(50) NULL,           -- 'two_piece_teamwork', etc.
    puzzle_order INT NOT NULL,             -- Order within module/collection
    difficulty ENUM('easy', 'medium', 'hard', 'expert') NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    fen_position VARCHAR(100) NOT NULL,    -- Starting board position
    solution_moves JSON NOT NULL,          -- Array of correct move sequences
    best_move_count INT NOT NULL,          -- Moves for 3 stars
    hint_text TEXT,
    INDEX idx_module (module),
    INDEX idx_collection (collection)
);

-- User progress on individual puzzles
CREATE TABLE puzzle_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    puzzle_id INT NOT NULL,
    stars_earned INT DEFAULT 0,            -- 0-3 stars
    best_moves INT NULL,                   -- Best number of moves to solve
    attempts INT DEFAULT 0,
    hints_used INT DEFAULT 0,
    first_solved_at TIMESTAMP NULL,
    last_attempted_at TIMESTAMP NULL,
    UNIQUE KEY uk_user_puzzle (user_id, puzzle_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id) ON DELETE CASCADE
);

-- Module/Collection unlock status
CREATE TABLE module_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    module_name VARCHAR(50) NOT NULL,
    is_unlocked BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,
    unlocked_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    UNIQUE KEY uk_user_module (user_id, module_name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Star balance and spending history
CREATE TABLE star_wallet (
    user_id INT PRIMARY KEY,
    total_earned INT DEFAULT 0,
    total_spent INT DEFAULT 0,
    current_balance INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Train station buildings owned
CREATE TABLE buildings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    building_type VARCHAR(50) NOT NULL,    -- 'ticket_booth', 'platform_1', etc.
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    position_x INT DEFAULT 0,
    position_y INT DEFAULT 0,
    customization JSON NULL,               -- Colors, upgrades, etc.
    UNIQUE KEY uk_user_building (user_id, building_type),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Decorations placed in station
CREATE TABLE decorations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    decoration_type VARCHAR(50) NOT NULL,  -- 'tree', 'bench', 'lamp', etc.
    position_x INT NOT NULL,
    position_y INT NOT NULL,
    rotation INT DEFAULT 0,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
);

-- Simple session tracking
CREATE TABLE sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    puzzles_solved INT DEFAULT 0,
    stars_earned INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, started_at)
);

-- Daily challenges
CREATE TABLE daily_challenges (
    id INT PRIMARY KEY AUTO_INCREMENT,
    challenge_date DATE UNIQUE NOT NULL,
    puzzle_id INT NOT NULL,
    bonus_stars INT DEFAULT 5,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id)
);

-- User daily challenge completions
CREATE TABLE daily_challenge_completions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_date DATE NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    stars_earned INT NOT NULL,
    UNIQUE KEY uk_user_date (user_id, challenge_date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Streak tracking
CREATE TABLE streaks (
    user_id INT PRIMARY KEY,
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    last_activity_date DATE NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## API Design

### Authentication (Simple)
```
POST /api/auth/login
  Body: { "username": "jamie" }
  Response: { "user_id": 1, "display_name": "Jamie", "session_token": "..." }

POST /api/auth/create-profile
  Body: { "username": "jamie", "display_name": "Jamie", "parent_id": null }
  Response: { "user_id": 1 }
```

### Puzzles
```
GET /api/puzzles/modules
  Response: [
    { "name": "pawn_power", "title": "Pawn Power", "puzzle_count": 15, "unlocked": true },
    { "name": "rook_railways", "title": "Rook Railways", "puzzle_count": 15, "unlocked": false }
  ]

GET /api/puzzles/module/:module_name
  Response: {
    "module": { "name": "pawn_power", "title": "Pawn Power" },
    "puzzles": [
      { "id": 1, "title": "Pawn Parade", "difficulty": "easy", "stars": 3 },
      { "id": 2, "title": "First Step", "difficulty": "easy", "stars": 0 }
    ]
  }

GET /api/puzzles/:id
  Response: {
    "id": 1,
    "title": "Pawn Parade",
    "fen": "8/8/8/8/8/8/P7/8 w - - 0 1",
    "goal": "Move the pawn forward!",
    "hint": "Pawns can move one or two squares on their first move.",
    "best_moves": 1
  }

POST /api/puzzles/:id/attempt
  Body: { "moves": ["a2a4"], "move_count": 1 }
  Response: { "correct": true, "stars": 3, "new_balance": 130 }

POST /api/puzzles/:id/hint
  Response: { "hint": "Try moving the pawn on a2" }
```

### Progress & Stars
```
GET /api/user/progress
  Response: {
    "total_stars": 127,
    "puzzles_solved": 45,
    "current_streak": 5,
    "modules_completed": ["pawn_power", "rook_railways"]
  }

GET /api/user/stars
  Response: { "earned": 150, "spent": 23, "balance": 127 }
```

### Train Station
```
GET /api/station
  Response: {
    "buildings": [
      { "type": "ticket_booth", "x": 100, "y": 200 }
    ],
    "decorations": [
      { "id": 1, "type": "tree", "x": 50, "y": 150 }
    ]
  }

POST /api/station/purchase
  Body: { "item_type": "building", "item_name": "snack_kiosk" }
  Response: { "success": true, "new_balance": 82, "item": {...} }

PUT /api/station/decoration/:id
  Body: { "x": 100, "y": 200, "rotation": 90 }
  Response: { "success": true }

DELETE /api/station/decoration/:id
  Response: { "success": true, "refund_stars": 3 }
```

### Daily Challenge
```
GET /api/daily-challenge
  Response: {
    "puzzle_id": 42,
    "bonus_stars": 5,
    "completed_today": false
  }

POST /api/daily-challenge/complete
  Body: { "moves": [...], "move_count": 3 }
  Response: { "stars_earned": 8, "streak": 6 }
```

---

## File/Folder Structure

```
chess_station_builder/
├── README.md
├── requirements.txt
├── run.py                          # Entry point
├── config.py                       # Configuration
│
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # SQLAlchemy models (all in one file)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── puzzles.py              # Puzzle routes
│   │   ├── station.py              # Train station routes
│   │   └── progress.py             # Progress & stats routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── puzzle_service.py       # Puzzle logic & validation
│   │   └── star_service.py         # Star calculations
│   └── utils/
│       ├── __init__.py
│       └── chess_validator.py      # python-chess wrapper
│
├── data/
│   ├── puzzles/
│   │   ├── module_pawn_power.json
│   │   ├── module_rook_railways.json
│   │   ├── module_bishops_boulevard.json
│   │   ├── module_knights_junction.json
│   │   ├── module_queens_station.json
│   │   ├── module_kings_keep.json
│   │   ├── collection_two_piece.json
│   │   ├── collection_defend_attack.json
│   │   └── ... (more collections)
│   ├── buildings.json              # Building definitions & costs
│   └── decorations.json            # Decoration definitions & costs
│
├── static/
│   ├── css/
│   │   ├── main.css
│   │   ├── chessboard.css
│   │   └── station.css
│   ├── js/
│   │   ├── app.js                  # Main application
│   │   ├── chess-board.js          # Board rendering
│   │   ├── puzzle-player.js        # Puzzle gameplay
│   │   ├── station-builder.js      # Station builder
│   │   ├── api-client.js           # API communication
│   │   └── lib/
│   │       └── chess.min.js        # chess.js library
│   ├── images/
│   │   ├── pieces/                 # Chess piece sprites
│   │   ├── buildings/              # Building sprites
│   │   ├── decorations/            # Decoration sprites
│   │   └── ui/                     # UI elements
│   └── audio/
│       ├── sfx/                    # Sound effects
│       └── music/                  # Background music
│
├── templates/
│   ├── index.html                  # Single page app shell
│   └── components/                 # HTML templates (optional)
│
├── scripts/
│   ├── init_db.py                  # Database initialization
│   ├── load_puzzles.py             # Load puzzles from JSON
│   └── seed_data.py                # Sample data for testing
│
└── tests/
    ├── test_puzzles.py
    ├── test_stars.py
    └── test_station.py
```

---

## Key Implementation Details

### Local Storage Backup
```javascript
// client-side backup for offline/crash recovery
const GameBackup = {
    save() {
        const state = {
            lastSave: Date.now(),
            currentPuzzle: game.currentPuzzle,
            pendingProgress: game.unsyncedProgress
        };
        localStorage.setItem('chess_station_backup', JSON.stringify(state));
    },

    restore() {
        const backup = localStorage.getItem('chess_station_backup');
        if (backup) {
            return JSON.parse(backup);
        }
        return null;
    },

    syncToServer() {
        const backup = this.restore();
        if (backup?.pendingProgress) {
            // Send unsynced progress to server
            api.syncProgress(backup.pendingProgress);
        }
    }
};

// Auto-save every 30 seconds
setInterval(() => GameBackup.save(), 30000);
```

### Simple Puzzle Validation
```python
# app/services/puzzle_service.py
import chess

def validate_solution(puzzle_fen, user_moves, correct_solution):
    """Validate user's solution against puzzle"""
    board = chess.Board(puzzle_fen)

    for i, move in enumerate(user_moves):
        try:
            chess_move = chess.Move.from_uci(move)
            if not board.is_legal(chess_move):
                return {"valid": False, "error": "Illegal move"}
            board.push(chess_move)
        except:
            return {"valid": False, "error": "Invalid move format"}

    # Check if solution matches any correct sequence
    if user_moves == correct_solution:
        return {"valid": True, "optimal": True}

    # Check if end position is correct (alternative solution)
    if is_puzzle_goal_achieved(board, puzzle_fen):
        return {"valid": True, "optimal": False}

    return {"valid": False, "error": "Incorrect solution"}

def calculate_stars(move_count, optimal_count):
    """Calculate stars based on efficiency"""
    if move_count <= optimal_count:
        return 3
    elif move_count <= optimal_count + 1:
        return 2
    else:
        return 1
```

---

## Deployment Options

### Option 1: Local Development (Simplest)
```bash
# Terminal 1: Run Flask server
cd chess_station_builder
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py

# Access at http://localhost:5000
```

### Option 2: Docker Compose (Easy Setup)
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql://user:pass@db/chess_station
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=chess_station
      - MYSQL_USER=user
      - MYSQL_PASSWORD=pass
      - MYSQL_ROOT_PASSWORD=rootpass
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

```bash
docker-compose up
```

---

## Pros and Cons

### Pros
1. **Fast Development**: Single developer can build MVP in 2-3 weeks
2. **Simple Deployment**: Run locally with one command, or use Docker
3. **Easy to Understand**: No complex architecture, everything in one place
4. **Low Overhead**: Minimal dependencies, small footprint
5. **Quick Iteration**: Change and test rapidly during prototyping
6. **Offline Backup**: LocalStorage provides crash protection
7. **No Build Step**: No webpack/bundlers, edit and refresh

### Cons
1. **Limited Scalability**: Single server, single database
2. **No Real-time Features**: REST only, no live updates
3. **Basic Security**: Simple authentication, not production-grade
4. **Manual Management**: No caching layer, no queue system
5. **Monolithic Code**: Everything coupled together
6. **Testing Complexity**: Harder to unit test without proper separation
7. **No CDN**: Static files served from Flask

---

## When to Choose This Solution

Choose **Solution 1 (Simple)** when:

- **Building a prototype** to test with your child
- **Solo developer** with limited time
- **Single family use** (1-3 users)
- **Local deployment** only (no public hosting)
- **Rapid iteration** is priority over polish
- **Budget is zero** (no cloud costs)
- **Learning the stack** while building

**Not recommended when:**
- You need multi-user access from different locations
- You want real-time features (multiplayer, live leaderboards)
- You plan to scale to many users
- You need enterprise-grade security

---

## Estimated Development Time

| Phase | Duration | Details |
|-------|----------|---------|
| Setup & Infrastructure | 2 days | Flask, MySQL, project structure |
| Database & Models | 2 days | Schema, SQLAlchemy models |
| Puzzle Engine | 3 days | Load puzzles, validation, star calculation |
| Chess Board UI | 4 days | Canvas rendering, piece movement |
| Train Station Builder | 4 days | Building placement, decorations |
| Progress System | 2 days | Modules, collections, unlocks |
| Star Economy | 1 day | Earning, spending, balance |
| Polish & Testing | 3 days | Bug fixes, testing with child |
| **Total** | **~3 weeks** | |

---

## Sample Code Snippets

### Flask App Factory
```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    CORS(app)
    db.init_app(app)

    from app.routes import auth, puzzles, station, progress
    app.register_blueprint(auth.bp)
    app.register_blueprint(puzzles.bp)
    app.register_blueprint(station.bp)
    app.register_blueprint(progress.bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
```

### Simple Chess Board (JavaScript)
```javascript
// static/js/chess-board.js
class ChessBoard {
    constructor(canvasId, size = 400) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.size = size;
        this.squareSize = size / 8;
        this.pieces = {};
        this.selectedSquare = null;

        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    draw() {
        // Draw board squares
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const isLight = (row + col) % 2 === 0;
                this.ctx.fillStyle = isLight ? '#f0d9b5' : '#b58863';
                this.ctx.fillRect(
                    col * this.squareSize,
                    row * this.squareSize,
                    this.squareSize,
                    this.squareSize
                );
            }
        }

        // Draw pieces
        for (const [square, piece] of Object.entries(this.pieces)) {
            this.drawPiece(square, piece);
        }

        // Highlight selected square
        if (this.selectedSquare) {
            this.highlightSquare(this.selectedSquare, 'rgba(255, 255, 0, 0.5)');
        }
    }

    loadPosition(fen) {
        // Parse FEN and populate this.pieces
        this.pieces = parseFEN(fen);
        this.draw();
    }

    handleClick(event) {
        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const col = Math.floor(x / this.squareSize);
        const row = Math.floor(y / this.squareSize);
        const square = String.fromCharCode(97 + col) + (8 - row);

        if (this.onSquareClick) {
            this.onSquareClick(square);
        }
    }
}
```

---

## Next Steps After MVP

Once the MVP is validated with your child:

1. **Gather Feedback**: What do they love? What frustrates them?
2. **Refine Puzzles**: Adjust difficulty based on real usage
3. **Add Polish**: Animations, sounds, more art
4. **Consider Upgrade**: Move to Solution 2 if you want to share with others

This simple architecture serves as an excellent foundation. The database schema is already production-ready, so upgrading to Solution 2 or 3 mainly involves the infrastructure layer, not data migration.
