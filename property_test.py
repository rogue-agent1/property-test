#!/usr/bin/env python3
"""Property-based testing: generators, shrinking, stateful testing."""
import sys, random, string

class Generator:
    @staticmethod
    def integer(lo=-1000, hi=1000): return random.randint(lo, hi)
    @staticmethod
    def string(min_len=0, max_len=20):
        n = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters, k=n))
    @staticmethod
    def list_of(gen, min_len=0, max_len=10):
        n = random.randint(min_len, max_len)
        return [gen() for _ in range(n)]
    @staticmethod
    def one_of(*values): return random.choice(values)
    @staticmethod
    def dictionary(key_gen, val_gen, min_size=0, max_size=5):
        n = random.randint(min_size, max_size)
        return {key_gen(): val_gen() for _ in range(n)}

class Shrinker:
    @staticmethod
    def shrink_int(n):
        if n == 0: return []
        candidates = [0, n//2, n-1, -n] if n > 0 else [0, n//2, n+1, -n]
        return [c for c in candidates if c != n]
    @staticmethod
    def shrink_list(lst):
        if not lst: return []
        candidates = [lst[1:], lst[:-1]]
        for i in range(len(lst)):
            candidates.append(lst[:i] + lst[i+1:])
        return candidates
    @staticmethod
    def shrink_string(s):
        if not s: return []
        return [s[1:], s[:-1], s[:len(s)//2]]

def property_test(name, gen_fn, prop_fn, n_tests=100, seed=42):
    random.seed(seed); failures = []
    for i in range(n_tests):
        args = gen_fn()
        try:
            if not prop_fn(*args if isinstance(args, tuple) else (args,)):
                failures.append({"test":i,"input":args})
        except Exception as e:
            failures.append({"test":i,"input":args,"error":str(e)})
    passed = n_tests - len(failures)
    return {"name":name,"passed":passed,"failed":len(failures),"total":n_tests,
            "failures":failures[:3]}

def main():
    # Property: sort is idempotent
    r1 = property_test("sort_idempotent",
        lambda: (Generator.list_of(lambda: Generator.integer(-100,100)),),
        lambda lst: sorted(sorted(lst)) == sorted(lst))
    print(f"  {r1['name']}: {r1['passed']}/{r1['total']} passed")
    # Property: reverse of reverse is identity
    r2 = property_test("reverse_reverse",
        lambda: (Generator.list_of(lambda: Generator.integer()),),
        lambda lst: list(reversed(list(reversed(lst)))) == lst)
    print(f"  {r2['name']}: {r2['passed']}/{r2['total']} passed")
    # Property: string encode/decode roundtrip
    r3 = property_test("encode_decode",
        lambda: (Generator.string(0, 50),),
        lambda s: s.encode('utf-8').decode('utf-8') == s)
    print(f"  {r3['name']}: {r3['passed']}/{r3['total']} passed")
    # Shrinking demo
    shrunk = Shrinker.shrink_int(42)
    print(f"  Shrink 42: {shrunk}")
    shrunk_list = Shrinker.shrink_list([1,2,3])
    print(f"  Shrink [1,2,3]: {shrunk_list}")

if __name__ == "__main__": main()
