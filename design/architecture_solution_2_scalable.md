# Architecture Solution 2: Scalable Production Architecture

## Overview

This solution prioritizes **scalability, maintainability, and production readiness**. It's designed for a small team, supports multiple concurrent users, and can grow with the application.

**Best For**: Production deployment, multiple users, cloud hosting, potential future growth

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (SPA)                                      │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                         React 18 + TypeScript                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │ │
│  │  │   Game UI    │  │ Chess Engine │  │   Station    │  │   Parent     │   │ │
│  │  │  Components  │  │  (chess.js)  │  │   Builder    │  │  Dashboard   │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      │ │
│  │  │ React Query  │  │  Zustand     │  │   Service    │   PWA + Offline     │ │
│  │  │ (API State)  │  │  (UI State)  │  │   Worker     │   IndexedDB Cache   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                      │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                         │
                              HTTPS (REST + WebSocket)
                                         │
┌────────────────────────────────────────┼────────────────────────────────────────┐
│                                        ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────────────┐ │
│  │                          NGINX (Reverse Proxy)                             │ │
│  │                    SSL Termination + Static Files + Load Balancing         │ │
│  └────────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                         │
│                 ┌──────────────────────┴──────────────────────┐                 │
│                 ▼                                              ▼                 │
│  ┌─────────────────────────────┐            ┌─────────────────────────────────┐ │
│  │      API Server (FastAPI)   │            │      API Server (FastAPI)       │ │
│  │  ┌───────────┐ ┌──────────┐ │            │  ┌───────────┐ ┌──────────┐     │ │
│  │  │  Routes   │ │  Auth    │ │            │  │  Routes   │ │  Auth    │     │ │
│  │  │  (REST)   │ │  (JWT)   │ │            │  │  (REST)   │ │  (JWT)   │     │ │
│  │  └───────────┘ └──────────┘ │            │  └───────────┘ └──────────┘     │ │
│  │  ┌───────────┐ ┌──────────┐ │            │  ┌───────────┐ ┌──────────┐     │ │
│  │  │  Services │ │ Pydantic │ │     x N    │  │  Services │ │ Pydantic │     │ │
│  │  │  Layer    │ │ Schemas  │ │            │  │  Layer    │ │ Schemas  │     │ │
│  │  └───────────┘ └──────────┘ │            │  └───────────┘ └──────────┘     │ │
│  └─────────────────────────────┘            └─────────────────────────────────┘ │
│                 │                                              │                 │
│                 └──────────────────────┬──────────────────────┘                 │
│                                        │                                         │
│                 ┌──────────────────────┼──────────────────────┐                 │
│                 ▼                      ▼                      ▼                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────────┐ │
│  │   MySQL Primary     │  │   Redis Cache       │  │   Celery Worker        │ │
│  │   (RDS/CloudSQL)    │  │   (Session/Cache)   │  │   (Background Tasks)   │ │
│  │                     │  │                     │  │                         │ │
│  │   MySQL Replica     │  └─────────────────────┘  └─────────────────────────┘ │
│  │   (Read Scaling)    │                                                        │
│  └─────────────────────┘                                                        │
│                                                                                  │
│                                    CLOUD PROVIDER                                │
│                           (AWS / GCP / DigitalOcean)                            │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
| Component | Technology | Why |
|-----------|------------|-----|
| Framework | React 18 + TypeScript | Type safety, large ecosystem, component reuse |
| Build Tool | Vite | Fast HMR, modern bundling |
| State (Server) | TanStack Query (React Query) | Caching, sync, optimistic updates |
| State (Client) | Zustand | Simple, performant, TypeScript-friendly |
| Chess Logic | chess.js + @nivo/chess | Client-side validation |
| Board UI | react-chessboard | Proven, customizable |
| Animations | Framer Motion | Smooth, kid-friendly animations |
| CSS | Tailwind CSS + CSS Modules | Utility-first, scoped styles |
| PWA | Workbox | Offline support, caching |
| Testing | Vitest + React Testing Library | Fast, modern testing |

### Backend
| Component | Technology | Why |
|-----------|------------|-----|
| Framework | FastAPI | Async, fast, auto-documentation, Pydantic |
| Auth | JWT + python-jose | Stateless, scalable auth |
| ORM | SQLAlchemy 2.0 (async) | Async support, mature ecosystem |
| Validation | Pydantic v2 | Fast validation, great DX |
| Chess | python-chess | Server-side puzzle validation |
| Task Queue | Celery + Redis | Background jobs (reports, daily challenges) |
| Caching | Redis | Session, API response caching |
| Testing | pytest + pytest-asyncio | Async test support |

### Database & Infrastructure
| Component | Technology | Why |
|-----------|------------|-----|
| Primary DB | MySQL 8.0 | As specified, with connection pooling |
| Cache/Session | Redis 7 | Fast in-memory cache |
| Reverse Proxy | NGINX | SSL, load balancing, static files |
| Container | Docker + Docker Compose | Consistent environments |
| Orchestration | Docker Compose (small) / K8s (large) | Scales with needs |
| CDN | CloudFlare / AWS CloudFront | Static asset delivery |

### Monitoring & DevOps
| Component | Technology | Purpose |
|-----------|------------|---------|
| Logging | Structlog + JSON | Structured, searchable logs |
| Metrics | Prometheus + Grafana | Performance monitoring |
| Error Tracking | Sentry | Error capture and alerting |
| CI/CD | GitHub Actions | Automated testing and deployment |

---

## Database Schema

```sql
-- ============================================
-- USERS & AUTHENTICATION
-- ============================================

CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) UNIQUE NOT NULL,           -- Public identifier
    email VARCHAR(255) UNIQUE,                -- Parent email (nullable for child)
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255),               -- NULL for child accounts
    display_name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    user_type ENUM('parent', 'child') NOT NULL DEFAULT 'child',
    parent_id BIGINT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_parent (parent_id),
    INDEX idx_user_type (user_type),
    INDEX idx_uuid (uuid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY,
    sound_volume INT DEFAULT 100 CHECK (sound_volume BETWEEN 0 AND 100),
    music_volume INT DEFAULT 80 CHECK (music_volume BETWEEN 0 AND 100),
    hint_mode ENUM('always', 'limited', 'earned') DEFAULT 'always',
    animation_speed ENUM('slow', 'normal', 'fast') DEFAULT 'normal',
    board_theme VARCHAR(30) DEFAULT 'classic',
    piece_theme VARCHAR(30) DEFAULT 'friendly',
    daily_time_limit_minutes INT,            -- NULL = unlimited
    notifications_enabled BOOLEAN DEFAULT TRUE,
    locale VARCHAR(10) DEFAULT 'en-US',
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE refresh_tokens (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    device_info VARCHAR(255),
    ip_address VARCHAR(45),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_expires (user_id, expires_at),
    INDEX idx_token_hash (token_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- PUZZLE CONTENT
-- ============================================

CREATE TABLE puzzle_modules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE NOT NULL,         -- 'pawn_power'
    title VARCHAR(100) NOT NULL,              -- 'Pawn Power'
    description TEXT,
    piece_focus VARCHAR(20),                  -- 'pawn', 'rook', etc.
    module_order INT NOT NULL,
    unlock_requirement JSON,                  -- { "type": "module_complete", "slug": "..." }
    building_reward VARCHAR(50),              -- Building unlocked on completion
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (module_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE puzzle_collections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    collection_order INT NOT NULL,
    difficulty_tier INT NOT NULL,             -- 1-5
    unlock_requirement JSON,
    building_reward VARCHAR(50),
    star_count_for_bonus INT DEFAULT 45,      -- Stars needed for bonus
    bonus_stars INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order (collection_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE puzzles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    uuid CHAR(36) UNIQUE NOT NULL,
    module_id INT,
    collection_id INT,
    puzzle_order INT NOT NULL,

    -- Puzzle content
    title VARCHAR(150) NOT NULL,
    description TEXT,
    goal_text VARCHAR(255) NOT NULL,          -- "Capture the rook!"
    difficulty ENUM('beginner', 'easy', 'medium', 'hard', 'expert') NOT NULL,

    -- Chess data
    fen_start VARCHAR(100) NOT NULL,
    solution_moves JSON NOT NULL,             -- [["e2e4", "e7e5", "d1h5"], [...]]
    best_move_count INT NOT NULL,
    side_to_move ENUM('white', 'black') NOT NULL,

    -- Hints
    hint_piece VARCHAR(10),                   -- Piece to highlight
    hint_text_1 VARCHAR(255),                 -- First hint
    hint_text_2 VARCHAR(255),                 -- Second hint (more specific)

    -- Metadata
    tags JSON,                                -- ["checkmate", "fork", "beginner"]
    source VARCHAR(100),                      -- Origin of puzzle
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (module_id) REFERENCES puzzle_modules(id) ON DELETE SET NULL,
    FOREIGN KEY (collection_id) REFERENCES puzzle_collections(id) ON DELETE SET NULL,
    INDEX idx_module_order (module_id, puzzle_order),
    INDEX idx_collection_order (collection_id, puzzle_order),
    INDEX idx_difficulty (difficulty),
    FULLTEXT idx_search (title, description, goal_text)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- USER PROGRESS
-- ============================================

CREATE TABLE puzzle_attempts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    puzzle_id BIGINT NOT NULL,

    -- Attempt details
    moves_played JSON NOT NULL,               -- User's move sequence
    move_count INT NOT NULL,
    time_spent_seconds INT,
    hints_used INT DEFAULT 0,

    -- Result
    is_solved BOOLEAN NOT NULL,
    is_optimal BOOLEAN DEFAULT FALSE,
    stars_earned INT DEFAULT 0 CHECK (stars_earned BETWEEN 0 AND 3),

    -- Context
    session_id BIGINT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id) ON DELETE CASCADE,
    INDEX idx_user_puzzle (user_id, puzzle_id),
    INDEX idx_user_date (user_id, attempted_at),
    INDEX idx_session (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE puzzle_progress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    puzzle_id BIGINT NOT NULL,

    -- Best performance
    best_stars INT DEFAULT 0 CHECK (best_stars BETWEEN 0 AND 3),
    best_moves INT,
    best_time_seconds INT,

    -- Stats
    total_attempts INT DEFAULT 0,
    total_hints_used INT DEFAULT 0,

    -- Timestamps
    first_attempted_at TIMESTAMP,
    first_solved_at TIMESTAMP,
    last_attempted_at TIMESTAMP,
    best_achieved_at TIMESTAMP,

    UNIQUE KEY uk_user_puzzle (user_id, puzzle_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id) ON DELETE CASCADE,
    INDEX idx_user_stars (user_id, best_stars)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE module_progress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    module_id INT NOT NULL,

    is_unlocked BOOLEAN DEFAULT FALSE,
    is_started BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,

    puzzles_completed INT DEFAULT 0,
    total_stars INT DEFAULT 0,
    perfect_stars BOOLEAN DEFAULT FALSE,     -- All 3-star

    unlocked_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    UNIQUE KEY uk_user_module (user_id, module_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES puzzle_modules(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE collection_progress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    collection_id INT NOT NULL,

    is_unlocked BOOLEAN DEFAULT FALSE,
    is_started BOOLEAN DEFAULT FALSE,
    is_completed BOOLEAN DEFAULT FALSE,

    puzzles_completed INT DEFAULT 0,
    total_stars INT DEFAULT 0,
    bonus_claimed BOOLEAN DEFAULT FALSE,

    unlocked_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    UNIQUE KEY uk_user_collection (user_id, collection_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (collection_id) REFERENCES puzzle_collections(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- STAR ECONOMY
-- ============================================

CREATE TABLE star_wallets (
    user_id BIGINT PRIMARY KEY,
    total_earned BIGINT DEFAULT 0,
    total_spent BIGINT DEFAULT 0,
    current_balance BIGINT DEFAULT 0,
    last_transaction_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE star_transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,

    -- Transaction details
    transaction_type ENUM('earn', 'spend', 'bonus', 'refund') NOT NULL,
    amount INT NOT NULL,
    balance_after BIGINT NOT NULL,

    -- Source/destination
    source_type VARCHAR(50),                  -- 'puzzle', 'daily_challenge', 'streak', etc.
    source_id VARCHAR(100),                   -- Puzzle ID, challenge ID, etc.
    description VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, created_at),
    INDEX idx_type (transaction_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- TRAIN STATION
-- ============================================

CREATE TABLE building_catalog (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('essential', 'luxury', 'decoration') NOT NULL,
    star_cost INT NOT NULL,
    unlock_requirement JSON,                  -- Module/collection to unlock
    sprite_key VARCHAR(100) NOT NULL,
    default_position JSON,                    -- { "x": 100, "y": 200 }
    size JSON,                                -- { "width": 64, "height": 64 }
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE decoration_catalog (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,            -- 'nature', 'infrastructure', 'fun', etc.
    star_cost INT NOT NULL,
    sprite_key VARCHAR(100) NOT NULL,
    size JSON,
    max_count INT,                            -- NULL = unlimited
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_buildings (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    building_id INT NOT NULL,

    position_x INT NOT NULL,
    position_y INT NOT NULL,
    customization JSON,                       -- Colors, upgrades, etc.

    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_user_building (user_id, building_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (building_id) REFERENCES building_catalog(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_decorations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    decoration_id INT NOT NULL,

    position_x INT NOT NULL,
    position_y INT NOT NULL,
    rotation INT DEFAULT 0,
    layer INT DEFAULT 0,                      -- Z-index for layering

    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (decoration_id) REFERENCES decoration_catalog(id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- SESSIONS & ENGAGEMENT
-- ============================================

CREATE TABLE game_sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,

    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INT,

    -- Activity summary
    puzzles_attempted INT DEFAULT 0,
    puzzles_solved INT DEFAULT 0,
    stars_earned INT DEFAULT 0,
    buildings_purchased INT DEFAULT 0,

    -- Device info
    device_type VARCHAR(20),                  -- 'desktop', 'tablet', 'mobile'
    user_agent VARCHAR(500),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, started_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE daily_challenges (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    challenge_date DATE UNIQUE NOT NULL,
    puzzle_id BIGINT NOT NULL,
    bonus_stars INT DEFAULT 5,
    theme VARCHAR(50),                        -- 'knight_day', 'checkmate_monday', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (puzzle_id) REFERENCES puzzles(id),
    INDEX idx_date (challenge_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE daily_challenge_completions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    challenge_id BIGINT NOT NULL,

    stars_earned INT NOT NULL,
    bonus_claimed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_user_challenge (user_id, challenge_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES daily_challenges(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_streaks (
    user_id BIGINT PRIMARY KEY,
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    last_activity_date DATE,
    streak_started_date DATE,

    -- Streak rewards tracking
    week_bonus_claimed_at DATE,               -- Last 7-day bonus claim

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    icon_key VARCHAR(100),
    star_reward INT DEFAULT 0,
    criteria JSON NOT NULL,                   -- { "type": "puzzles_solved", "count": 100 }
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_achievements (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    achievement_id INT NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_user_achievement (user_id, achievement_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

CREATE VIEW v_user_stats AS
SELECT
    u.id AS user_id,
    COALESCE(sw.current_balance, 0) AS star_balance,
    COALESCE(sw.total_earned, 0) AS total_stars_earned,
    COUNT(DISTINCT pp.puzzle_id) AS puzzles_attempted,
    COUNT(DISTINCT CASE WHEN pp.best_stars > 0 THEN pp.puzzle_id END) AS puzzles_solved,
    COUNT(DISTINCT CASE WHEN pp.best_stars = 3 THEN pp.puzzle_id END) AS puzzles_perfected,
    COALESCE(us.current_streak, 0) AS current_streak,
    COALESCE(us.longest_streak, 0) AS longest_streak
FROM users u
LEFT JOIN star_wallets sw ON u.id = sw.user_id
LEFT JOIN puzzle_progress pp ON u.id = pp.user_id
LEFT JOIN user_streaks us ON u.id = us.user_id
GROUP BY u.id, sw.current_balance, sw.total_earned, us.current_streak, us.longest_streak;
```

---

## API Design

### Base URL & Versioning
```
Base URL: https://api.chessstation.app/v1
```

### Authentication
```
POST /auth/register
  Body: { "email": "parent@email.com", "password": "...", "display_name": "Parent" }
  Response: { "user": {...}, "access_token": "...", "refresh_token": "..." }

POST /auth/login
  Body: { "email": "...", "password": "..." }
  Response: { "user": {...}, "access_token": "...", "refresh_token": "..." }

POST /auth/refresh
  Body: { "refresh_token": "..." }
  Response: { "access_token": "...", "refresh_token": "..." }

POST /auth/logout
  Headers: Authorization: Bearer <token>
  Response: { "success": true }

POST /auth/child-profile
  Headers: Authorization: Bearer <token>  (parent token)
  Body: { "username": "jamie", "display_name": "Jamie", "avatar_url": "..." }
  Response: { "user": {...}, "pin_code": "1234" }

POST /auth/child-login
  Body: { "username": "jamie", "pin_code": "1234" }
  Response: { "user": {...}, "access_token": "..." }
```

### Users
```
GET /users/me
  Response: {
    "id": "uuid",
    "username": "jamie",
    "display_name": "Jamie",
    "user_type": "child",
    "stats": {
      "star_balance": 127,
      "puzzles_solved": 45,
      "current_streak": 5
    },
    "settings": {...}
  }

PATCH /users/me
  Body: { "display_name": "Jamie Star", "avatar_url": "..." }
  Response: { "user": {...} }

GET /users/me/settings
PATCH /users/me/settings
  Body: { "sound_volume": 80, "hint_mode": "limited" }
```

### Puzzles
```
GET /puzzles/modules
  Response: {
    "modules": [
      {
        "id": 1,
        "slug": "pawn_power",
        "title": "Pawn Power",
        "piece_focus": "pawn",
        "puzzle_count": 15,
        "progress": {
          "is_unlocked": true,
          "puzzles_completed": 10,
          "total_stars": 28,
          "is_completed": false
        }
      }
    ]
  }

GET /puzzles/collections
  Response: { "collections": [...] }

GET /puzzles/modules/:slug
  Response: {
    "module": {...},
    "puzzles": [
      {
        "id": "puzzle-uuid",
        "title": "Pawn Parade",
        "difficulty": "easy",
        "user_progress": { "best_stars": 3, "attempts": 2 }
      }
    ]
  }

GET /puzzles/:uuid
  Response: {
    "id": "puzzle-uuid",
    "title": "Pawn Parade",
    "fen": "8/8/8/8/8/8/P7/8 w - - 0 1",
    "goal_text": "Move the pawn forward!",
    "side_to_move": "white",
    "best_move_count": 1,
    "user_progress": {...}
  }

POST /puzzles/:uuid/attempts
  Body: {
    "moves": ["a2a4"],
    "time_spent_seconds": 15,
    "hints_used": 0
  }
  Response: {
    "is_solved": true,
    "is_optimal": true,
    "stars_earned": 3,
    "is_new_best": true,
    "rewards": {
      "stars_added": 3,
      "new_balance": 130,
      "achievements_unlocked": []
    }
  }

GET /puzzles/:uuid/hints
  Query: ?level=1  (1 or 2)
  Response: {
    "hint_level": 1,
    "hint_piece": "a2",
    "hint_text": "Try moving the pawn on a2"
  }
```

### Progress
```
GET /progress/overview
  Response: {
    "stars": { "earned": 150, "spent": 23, "balance": 127 },
    "puzzles": { "total": 340, "solved": 45, "perfected": 30 },
    "modules": { "total": 6, "completed": 2 },
    "collections": { "total": 8, "unlocked": 1, "completed": 0 },
    "streak": { "current": 5, "longest": 12 },
    "time_played_minutes": 195
  }

GET /progress/history
  Query: ?from=2024-01-01&to=2024-01-31
  Response: {
    "daily_activity": [
      { "date": "2024-01-15", "puzzles_solved": 5, "stars_earned": 12, "minutes": 15 }
    ]
  }
```

### Train Station
```
GET /station
  Response: {
    "buildings": [
      { "id": 1, "slug": "ticket_booth", "x": 100, "y": 200, "customization": {} }
    ],
    "decorations": [
      { "id": 1, "slug": "tree_oak", "x": 50, "y": 150, "rotation": 0 }
    ],
    "available_buildings": [...],
    "available_decorations": [...]
  }

POST /station/buildings
  Body: { "building_slug": "snack_kiosk" }
  Response: {
    "building": {...},
    "transaction": { "cost": 45, "new_balance": 82 }
  }

POST /station/decorations
  Body: { "decoration_slug": "tree_oak", "x": 100, "y": 200 }
  Response: { "decoration": {...}, "transaction": {...} }

PATCH /station/decorations/:id
  Body: { "x": 120, "y": 210, "rotation": 45 }
  Response: { "decoration": {...} }

DELETE /station/decorations/:id
  Response: { "refund": { "amount": 3, "new_balance": 85 } }
```

### Daily Challenge
```
GET /challenges/daily
  Response: {
    "challenge_date": "2024-01-15",
    "puzzle": {...},
    "bonus_stars": 5,
    "theme": "Knight Day",
    "user_status": { "completed": false }
  }

POST /challenges/daily/complete
  Body: { "moves": [...], "time_spent_seconds": 45 }
  Response: {
    "stars_earned": 8,
    "streak_bonus": 0,
    "new_streak": 6,
    "rewards": {...}
  }
```

### Parent Dashboard
```
GET /parent/children
  Response: {
    "children": [
      { "id": "...", "display_name": "Jamie", "last_active": "...", "stats": {...} }
    ]
  }

GET /parent/children/:id/progress
  Response: { "detailed_progress": {...} }

GET /parent/children/:id/sessions
  Query: ?limit=10
  Response: { "sessions": [...] }

PATCH /parent/children/:id/settings
  Body: { "daily_time_limit_minutes": 30, "hint_mode": "limited" }
```

---

## File/Folder Structure

```
chess-station-builder/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-staging.yml
│       └── deploy-prod.yml
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   ├── public/
│   │   ├── manifest.json
│   │   ├── sw.js
│   │   └── icons/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── api/
│   │   │   ├── client.ts               # Axios instance
│   │   │   ├── auth.ts
│   │   │   ├── puzzles.ts
│   │   │   ├── station.ts
│   │   │   └── progress.ts
│   │   │
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── StarDisplay.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── chess/
│   │   │   │   ├── ChessBoard.tsx
│   │   │   │   ├── PieceSprite.tsx
│   │   │   │   ├── MoveHighlight.tsx
│   │   │   │   └── VictoryAnimation.tsx
│   │   │   ├── station/
│   │   │   │   ├── StationCanvas.tsx
│   │   │   │   ├── BuildingSprite.tsx
│   │   │   │   ├── DecorationPlacer.tsx
│   │   │   │   └── BuildMenu.tsx
│   │   │   └── layout/
│   │   │       ├── Header.tsx
│   │   │       ├── Navigation.tsx
│   │   │       └── Footer.tsx
│   │   │
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── ChildSelector.tsx
│   │   │   │   └── useAuth.ts
│   │   │   ├── puzzles/
│   │   │   │   ├── PuzzlePlayer.tsx
│   │   │   │   ├── ModuleList.tsx
│   │   │   │   ├── PuzzleList.tsx
│   │   │   │   ├── HintSystem.tsx
│   │   │   │   └── usePuzzle.ts
│   │   │   ├── station/
│   │   │   │   ├── StationBuilder.tsx
│   │   │   │   ├── Shop.tsx
│   │   │   │   └── useStation.ts
│   │   │   └── progress/
│   │   │       ├── ProgressDashboard.tsx
│   │   │       ├── AchievementList.tsx
│   │   │       └── StreakDisplay.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Play.tsx
│   │   │   ├── Station.tsx
│   │   │   ├── Progress.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── ParentDashboard.tsx
│   │   │
│   │   ├── stores/
│   │   │   ├── authStore.ts
│   │   │   ├── gameStore.ts
│   │   │   └── uiStore.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── useOffline.ts
│   │   │   └── useSound.ts
│   │   │
│   │   ├── utils/
│   │   │   ├── chess.ts
│   │   │   ├── stars.ts
│   │   │   └── format.ts
│   │   │
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   └── themes/
│   │   │
│   │   └── types/
│   │       ├── api.ts
│   │       ├── chess.ts
│   │       └── station.ts
│   │
│   └── tests/
│       ├── setup.ts
│       ├── components/
│       └── features/
│
├── backend/
│   ├── pyproject.toml
│   ├── poetry.lock
│   ├── alembic.ini
│   ├── Dockerfile
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app
│   │   ├── config.py                   # Settings (pydantic-settings)
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py                 # Dependencies (auth, db)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py           # API router
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── puzzles.py
│   │   │       ├── progress.py
│   │   │       ├── station.py
│   │   │       ├── challenges.py
│   │   │       └── parent.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py             # JWT, hashing
│   │   │   ├── exceptions.py           # Custom exceptions
│   │   │   └── middleware.py           # Request logging, etc.
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── session.py              # Async session
│   │   │   └── base.py                 # Base model
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── puzzle.py
│   │   │   ├── progress.py
│   │   │   ├── station.py
│   │   │   └── engagement.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── puzzle.py
│   │   │   ├── progress.py
│   │   │   ├── station.py
│   │   │   └── common.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── puzzle_service.py
│   │   │   ├── star_service.py
│   │   │   ├── station_service.py
│   │   │   ├── progress_service.py
│   │   │   └── achievement_service.py
│   │   │
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py
│   │   │   └── tasks/
│   │   │       ├── daily_challenge.py
│   │   │       ├── streak_check.py
│   │   │       └── reports.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── chess_validator.py
│   │
│   ├── migrations/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── data/
│   │   ├── puzzles/
│   │   │   └── *.json
│   │   ├── buildings.json
│   │   ├── decorations.json
│   │   └── achievements.json
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_puzzles.py
│       ├── test_stars.py
│       └── test_station.py
│
├── infrastructure/
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   ├── mysql/
│   │   └── init.sql
│   └── redis/
│       └── redis.conf
│
└── docs/
    ├── api.md
    ├── deployment.md
    └── architecture.md
```

---

## Key Implementation Details

### Offline Support with Service Worker
```typescript
// frontend/public/sw.js
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, CacheFirst } from 'workbox-strategies';

// Precache static assets
precacheAndRoute(self.__WB_MANIFEST);

// Cache API responses for offline
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/puzzles'),
  new StaleWhileRevalidate({
    cacheName: 'puzzle-cache',
    plugins: [
      new ExpirationPlugin({ maxEntries: 500 }),
    ],
  })
);

// Cache images
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'image-cache',
    plugins: [
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 30 * 24 * 60 * 60 }),
    ],
  })
);
```

### React Query for Data Fetching
```typescript
// frontend/src/features/puzzles/usePuzzle.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { puzzleApi } from '@/api/puzzles';

export function usePuzzle(puzzleId: string) {
  return useQuery({
    queryKey: ['puzzle', puzzleId],
    queryFn: () => puzzleApi.getPuzzle(puzzleId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useSubmitAttempt(puzzleId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (attempt: PuzzleAttempt) => puzzleApi.submitAttempt(puzzleId, attempt),
    onSuccess: (result) => {
      // Update puzzle progress in cache
      queryClient.setQueryData(['puzzle', puzzleId], (old: Puzzle) => ({
        ...old,
        user_progress: {
          ...old.user_progress,
          best_stars: Math.max(old.user_progress?.best_stars || 0, result.stars_earned),
        },
      }));

      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['progress'] });
      queryClient.invalidateQueries({ queryKey: ['stars'] });
    },
  });
}
```

### FastAPI Dependency Injection
```python
# backend/app/api/deps.py
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.core.security import verify_token
from app.models import User
from app.services import UserService

security = HTTPBearer()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_service = UserService(db)
    user = await user_service.get_by_uuid(payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user

async def get_current_parent(
    user: User = Depends(get_current_user)
) -> User:
    if user.user_type != "parent":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
```

### Celery Background Tasks
```python
# backend/app/workers/tasks/daily_challenge.py
from celery import shared_task
from datetime import date, timedelta
import random

from app.db.session import sync_session_maker
from app.models import DailyChallenge, Puzzle

@shared_task
def generate_daily_challenge():
    """Generate tomorrow's daily challenge at midnight"""
    with sync_session_maker() as db:
        tomorrow = date.today() + timedelta(days=1)

        # Check if already exists
        existing = db.query(DailyChallenge).filter(
            DailyChallenge.challenge_date == tomorrow
        ).first()

        if existing:
            return {"status": "already_exists"}

        # Select a random medium-difficulty puzzle
        puzzles = db.query(Puzzle).filter(
            Puzzle.difficulty.in_(['easy', 'medium']),
            Puzzle.is_active == True
        ).all()

        selected = random.choice(puzzles)

        challenge = DailyChallenge(
            challenge_date=tomorrow,
            puzzle_id=selected.id,
            bonus_stars=5
        )
        db.add(challenge)
        db.commit()

        return {"status": "created", "puzzle_id": selected.id}
```

---

## Deployment Architecture

### Docker Compose (Development/Small Scale)
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
    environment:
      - VITE_API_URL=http://localhost:8000

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app
    environment:
      - DATABASE_URL=mysql+asyncmy://user:pass@db:3306/chess_station
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    depends_on:
      - db
      - redis

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.workers.celery_app worker -l info
    environment:
      - DATABASE_URL=mysql+asyncmy://user:pass@db:3306/chess_station
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.workers.celery_app beat -l info
    depends_on:
      - redis

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=chess_station
      - MYSQL_USER=user
      - MYSQL_PASSWORD=pass
      - MYSQL_ROOT_PASSWORD=rootpass
    volumes:
      - mysql_data:/var/lib/mysql
      - ./infrastructure/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend

volumes:
  mysql_data:
  redis_data:
```

### Cloud Deployment (AWS Example)
```
┌─────────────────────────────────────────────────────────────────┐
│                         Route 53 (DNS)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CloudFront (CDN)                            │
│                 Static assets from S3                           │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Application Load Balancer                       │
│                    SSL Termination                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┴───────────────┐
                ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   ECS Fargate (API)     │     │   ECS Fargate (API)     │
│   FastAPI Container     │     │   FastAPI Container     │
└─────────────────────────┘     └─────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│  RDS MySQL    │     │  ElastiCache  │     │ ECS (Celery)  │
│  Primary +    │     │  (Redis)      │     │  Workers      │
│  Read Replica │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
```

---

## Pros and Cons

### Pros
1. **Production Ready**: Proper auth, security, monitoring
2. **Scalable**: Horizontal scaling with load balancer
3. **Maintainable**: Clean separation of concerns
4. **Type Safe**: TypeScript + Pydantic catch errors early
5. **Offline Support**: PWA with service worker
6. **Fast Development**: React ecosystem, hot reload
7. **API Documentation**: Auto-generated OpenAPI docs
8. **Background Jobs**: Celery handles async tasks
9. **Caching**: Redis improves response times
10. **Team Ready**: Multiple developers can work in parallel

### Cons
1. **More Complex**: More moving parts to manage
2. **Higher Cost**: Need Redis, multiple containers
3. **Longer Setup**: 1-2 weeks before productive
4. **Learning Curve**: React, FastAPI, Docker knowledge needed
5. **Overkill for MVP**: More than needed for single user
6. **DevOps Required**: Need to manage infrastructure

---

## When to Choose This Solution

Choose **Solution 2 (Scalable)** when:

- **Multiple users** will access the application
- **Cloud deployment** is planned
- **Small team** (2-4 developers)
- **Production quality** is required
- **Future growth** is anticipated
- **Offline support** is important
- **Parent dashboard** with analytics needed
- **Moderate budget** available for hosting

**Not recommended when:**
- Building quick prototype for single user
- No team/DevOps experience
- Zero budget for cloud hosting
- Need real-time multiplayer features

---

## Estimated Development Time

| Phase | Duration | Details |
|-------|----------|---------|
| Project Setup | 3 days | Docker, CI/CD, project structure |
| Database & Models | 3 days | Schema, migrations, SQLAlchemy |
| Auth System | 3 days | JWT, parent/child accounts |
| Puzzle API | 4 days | CRUD, validation, progress |
| React Setup | 2 days | Vite, routing, state management |
| Chess Board UI | 5 days | react-chessboard, animations |
| Station Builder | 5 days | Canvas, building placement |
| Star Economy | 2 days | Transactions, balance |
| PWA & Offline | 3 days | Service worker, IndexedDB |
| Parent Dashboard | 3 days | Stats, settings, reports |
| Celery Tasks | 2 days | Daily challenges, streaks |
| Testing | 4 days | Unit, integration, E2E |
| Deployment | 3 days | Docker, cloud setup |
| **Total** | **~6 weeks** | |

---

## Migration Path from Solution 1

If you start with Solution 1 and want to upgrade:

1. **Database**: Schema is compatible, use Alembic for migrations
2. **API**: Rewrite routes in FastAPI (same endpoints)
3. **Frontend**: Rebuild in React (reuse logic)
4. **Data**: Export/import JSON, no data loss

The database schema in both solutions is designed for forward compatibility.
