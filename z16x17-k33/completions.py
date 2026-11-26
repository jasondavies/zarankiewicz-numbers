"""Test extensions of one complete catalogue of nine-point projections."""
from functools import lru_cache
from itertools import combinations


class Extensions:
    def __init__(self, positions):
        self.n = positions
        # Bit m denotes the candidate line whose support is the binary mask m.
        count = 1 << positions
        self.weights = [bytearray(count // 8) for _ in range(positions + 1)]
        for m in range(count):
            self.weights[m.bit_count()][m//8] |= 1 << (m%8)
        self.weights = [int.from_bytes(s, 'little') for s in self.weights]
        universe = (1 << count) - 1
        # For coordinate j, presence alternates in runs of 2**j indices.
        positions_on = [universe // ((1 << (1 << j)) + 1) << (1 << j)
                        for j in range(positions)]
        self.triple_bans = {(1<<i) | (1<<j) | (1<<k): positions_on[i] & positions_on[j] & positions_on[k]
                            for i,j,k in combinations(range(positions),3)}

    @lru_cache(maxsize=4096)
    def forbidden(self, common):
        """Candidate lines containing at least three coordinates of common."""
        banned = 0
        points = [1<<j for j in range(self.n) if common & (1<<j)]
        for a,b,c in combinations(points,3):
            banned |= self.triple_bans[a | b | c]
        return banned

    def choose(self, available, fixed, k, total, low, high):
        if k == 0:
            return fixed if total == 0 else None
        upper = 0
        left = k
        for d in range(high, low-1, -1):
            take = min(left, (available & self.weights[d]).bit_count())
            upper += take*d
            left -= take
            if not left:
                break
        if left or upper < total:
            return None
        for d in range(min(high,total-(k-1)*low), max(low, (total+k-1)//k)-1, -1):
            layer = available & self.weights[d]
            # Later choices have weight at most d. Equal-weight choices are
            # taken in descending numeric order to remove ordering duplicates.
            while layer:
                m = layer.bit_length()-1
                bit = 1 << m
                layer ^= bit
                available ^= bit
                next_available = available
                for r in fixed:
                    next_available &= ~self.forbidden(r & m)
                answer = self.choose(next_available, fixed+(m,), k-1, total-d, low, d)
                if answer is not None:
                    return answer
        return None

    def complete(self, blocks, column, weight=133):
        k, low = (7,7) if column else (8,6)
        high = self.n if column else 8
        assert len(blocks)==self.n and all(0<=b<512 for b in blocks)
        assert all((a & b).bit_count()<=2 for a,b in combinations(blocks,2))
        fixed = tuple(sum(((b>>j)&1)<<i for i,b in enumerate(blocks)) for j in range(9))
        total = weight-9-sum(x.bit_count() for x in fixed)
        available = sum(self.weights[low:high+1])
        for a,b in combinations(fixed,2):
            available &= ~self.forbidden(a & b)
        # A tighter actual maximum often forces several maximum-weight lines.
        while high>=low and not available & self.weights[high]:
            high -= 1
        if high < low or k*high<total:
            return None
        need_high = total-k*(high-1)
        if need_high>0:
            top = available & self.weights[high]
            if self.choose(top, fixed, need_high, need_high*high, high, high) is None:
                return None
        result = self.choose(available, fixed, k, total, low, high)
        if result is None:
            return None
        full = [r | ((1<<self.n) if i<9 else 0) for i,r in enumerate(result)]
        rows = full if column else [sum(((x>>j)&1)<<i for i,x in enumerate(full)) for j in range(16)]
        assert len(rows)==16 and sum(x.bit_count() for x in rows)==weight
        assert all((a&b&c).bit_count()<=2 for a,b,c in combinations(rows,3))
        return rows
