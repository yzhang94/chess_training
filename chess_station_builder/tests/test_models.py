from datetime import date

from app.models import (
    DailyChallenge,
    DailyChallengeCompletion,
    ModuleProgress,
    Puzzle,
    PuzzleProgress,
    StarWallet,
    User,
    UserSettings,
)


def test_user_settings_relationship(session):
    user = User(username="jamie", display_name="Jamie")
    session.add(user)
    session.flush()

    settings = UserSettings(user_id=user.id, theme="classic")
    session.add(settings)
    session.commit()

    refreshed_user = session.get(User, user.id)
    assert refreshed_user.settings.theme == "classic"


def test_puzzle_progress_unique_constraint(session):
    user = User(username="alex", display_name="Alex")
    puzzle = Puzzle(
        module="pawn_power",
        collection=None,
        puzzle_order=1,
        difficulty="easy",
        title="Pawn Parade",
        description=None,
        fen_position="8/8/8/8/8/8/P7/8 w - - 0 1",
        solution_moves={"moves": ["a2a4"]},
        best_move_count=1,
        hint_text="Try moving the pawn on a2",
    )
    session.add_all([user, puzzle])
    session.flush()

    progress = PuzzleProgress(user_id=user.id, puzzle_id=puzzle.id, stars_earned=3)
    session.add(progress)
    session.commit()

    duplicate = PuzzleProgress(user_id=user.id, puzzle_id=puzzle.id, stars_earned=2)
    session.add(duplicate)

    try:
        session.commit()
        assert False, "Expected unique constraint violation"
    except Exception:
        session.rollback()


def test_daily_challenge_completion(session):
    user = User(username="sam", display_name="Sam")
    puzzle = Puzzle(
        module="rook_railways",
        collection=None,
        puzzle_order=2,
        difficulty="medium",
        title="Rook Route",
        description=None,
        fen_position="8/8/8/8/8/8/R7/8 w - - 0 1",
        solution_moves={"moves": ["a2a3"]},
        best_move_count=1,
        hint_text="Rooks move in straight lines",
    )
    session.add_all([user, puzzle])
    session.flush()

    challenge = DailyChallenge(challenge_date=date(2024, 1, 1), puzzle_id=puzzle.id)
    completion = DailyChallengeCompletion(
        user_id=user.id,
        challenge_date=date(2024, 1, 1),
        stars_earned=8,
    )
    wallet = StarWallet(user_id=user.id, total_earned=8, current_balance=8)
    module_progress = ModuleProgress(user_id=user.id, module_name="rook_railways")

    session.add_all([challenge, completion, wallet, module_progress])
    session.commit()

    fetched = session.get(DailyChallengeCompletion, completion.id)
    assert fetched.stars_earned == 8
