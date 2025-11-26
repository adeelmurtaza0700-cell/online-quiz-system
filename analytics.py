from database import fetch_all

def statistics(quiz_id):
    results = fetch_all("SELECT score FROM results WHERE quiz_id=%s",(quiz_id,))
    scores = [r['score'] for r in results]
    total = len(scores)
    passed = len([s for s in scores if s>=50])
    failed = total - passed
    avg = sum(scores)/total if total else 0
    return {"total":total,"passed":passed,"failed":failed,"average":avg}
