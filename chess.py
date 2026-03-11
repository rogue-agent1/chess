#!/usr/bin/env python3
"""Chess engine with minimax + alpha-beta."""
import sys
PIECES={'P':1,'N':3,'B':3,'R':5,'Q':9,'K':100,'p':-1,'n':-3,'b':-3,'r':-5,'q':-9,'k':-100}
INIT=['rnbqkbnr','pppppppp','........','........','........','........','PPPPPPPP','RNBQKBNR']
def board_from(rows): return [list(r) for r in rows]
def display(b):
    for i,row in enumerate(b): print(f"  {8-i} {''.join(row)}")
    print("    abcdefgh")
def evaluate(b): return sum(PIECES.get(b[r][c],0) for r in range(8) for c in range(8))
def moves(b,white):
    mvs=[]
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p=='.' or (white and p.islower()) or (not white and p.isupper()): continue
            if p.upper()=='P':
                d=-1 if p.isupper() else 1
                if 0<=r+d<8 and b[r+d][c]=='.': mvs.append((r,c,r+d,c))
                for dc in [-1,1]:
                    if 0<=r+d<8 and 0<=c+dc<8 and b[r+d][c+dc]!='.' and b[r+d][c+dc].islower()!=p.islower():
                        mvs.append((r,c,r+d,c+dc))
            elif p.upper()=='N':
                for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<8 and 0<=nc<8 and (b[nr][nc]=='.' or b[nr][nc].islower()!=p.islower()):
                        mvs.append((r,c,nr,nc))
            elif p.upper() in 'BRQ':
                dirs=[]
                if p.upper() in 'BQ': dirs+=[(-1,-1),(-1,1),(1,-1),(1,1)]
                if p.upper() in 'RQ': dirs+=[(-1,0),(1,0),(0,-1),(0,1)]
                for dr,dc in dirs:
                    nr,nc=r+dr,c+dc
                    while 0<=nr<8 and 0<=nc<8:
                        if b[nr][nc]=='.': mvs.append((r,c,nr,nc))
                        elif b[nr][nc].islower()!=p.islower(): mvs.append((r,c,nr,nc)); break
                        else: break
                        nr+=dr; nc+=dc
            elif p.upper()=='K':
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if dr==0 and dc==0: continue
                        nr,nc=r+dr,c+dc
                        if 0<=nr<8 and 0<=nc<8 and (b[nr][nc]=='.' or b[nr][nc].islower()!=p.islower()):
                            mvs.append((r,c,nr,nc))
    return mvs
def make_move(b,m):
    nb=[r[:] for r in b]; r1,c1,r2,c2=m
    nb[r2][c2]=nb[r1][c1]; nb[r1][c1]='.'
    return nb
def minimax(b,depth,alpha,beta,white):
    if depth==0: return evaluate(b),None
    mvs=moves(b,white)
    if not mvs: return evaluate(b),None
    best_m=mvs[0]
    if white:
        val=-999
        for m in mvs:
            v,_=minimax(make_move(b,m),depth-1,alpha,beta,False)
            if v>val: val=v; best_m=m
            alpha=max(alpha,v)
            if alpha>=beta: break
    else:
        val=999
        for m in mvs:
            v,_=minimax(make_move(b,m),depth-1,alpha,beta,True)
            if v<val: val=v; best_m=m
            beta=min(beta,v)
            if alpha>=beta: break
    return val,best_m
b=board_from(INIT); display(b)
val,m=minimax(b,3,-999,999,True)
if m:
    r1,c1,r2,c2=m
    print(f"\nBest move (white, depth=3): {chr(c1+97)}{8-r1}{chr(c2+97)}{8-r2} (eval={val})")
