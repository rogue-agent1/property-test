#!/usr/bin/env python3
"""Property-based testing (like Hypothesis, from scratch)."""
import sys,random,string
def gen_int(lo=-1000,hi=1000): return random.randint(lo,hi)
def gen_float(lo=-1e6,hi=1e6): return random.uniform(lo,hi)
def gen_str(max_len=20):
    n=random.randint(0,max_len)
    return ''.join(random.choice(string.printable) for _ in range(n))
def gen_list(gen=gen_int,max_len=20):
    n=random.randint(0,max_len)
    return [gen() for _ in range(n)]
def forall(gen,prop,n=100):
    for i in range(n):
        val=gen()
        try:
            if not prop(val):
                return {"status":"FAIL","counterexample":val,"iteration":i}
        except Exception as e:
            return {"status":"ERROR","counterexample":val,"error":str(e),"iteration":i}
    return {"status":"PASS","iterations":n}
def main():
    random.seed(42)
    tests=[
        ("sort is idempotent",lambda:gen_list(),lambda xs:sorted(sorted(xs))==sorted(xs)),
        ("reverse twice = identity",lambda:gen_list(),lambda xs:list(reversed(list(reversed(xs))))==xs),
        ("len(a+b) = len(a)+len(b)",lambda:(gen_str(),gen_str()),lambda t:len(t[0]+t[1])==len(t[0])+len(t[1])),
        ("abs(x) >= 0",gen_int,lambda x:abs(x)>=0),
        ("x+0 = x (int)",gen_int,lambda x:x+0==x),
    ]
    for name,gen,prop in tests:
        result=forall(gen,prop,n=200)
        status="✓" if result["status"]=="PASS" else "✗"
        print(f"  {status} {name}: {result['status']}")
        if result["status"]!="PASS": print(f"    Counterexample: {result.get('counterexample')}")
if __name__=="__main__": main()
