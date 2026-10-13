from nms_namegen.prng import PRNG
from nms_namegen.system import CONST_A, CONST_B

MASK64 = 0xFFFFFFFFFFFFFFFF


def sellBuy(portal_code, galaxy):
    """Sell% and buy% shown on the galaxy map for a system.

    They are the first two draws of the same PRNG stream planetSeeds() uses:
        buy  = -30 + 20 * u1
        sell =  40 + 40 * u2
    where u_k is the low 32 bits of the seed after k updates, divided by 2**32.
    The planet digit of portal_code is ignored. Values are rounded to 1 decimal,
    as the game shows them.
    """
    galacticCoords = portal_code & 0xFFFFFFFF
    systemIndex = ((portal_code & 0x0FFF00000000) >> 24) | galaxy

    register = (systemIndex << 0x20) | galacticCoords
    register = (((register >> 33) ^ register) * CONST_A) & MASK64
    register = (((register >> 33) ^ register) * CONST_B) & MASK64
    register = (register >> 33) ^ register

    seed_h = (
        (((register & 0xFFFF0000) >> 16) | ((register & 0x0000FFFF) << 16))
        ^ (register & 0xFFFFFFFF)
        ^ (register >> 32)
    )
    if seed_h == 0:
        seed_h = 1
    rng = PRNG(seed_h << 32 | (register & 0xFFFFFFFF))

    u1 = rng.randi() / 2**32
    u2 = rng.randi() / 2**32
    return {"sell": round(40 + 40 * u2, 1), "buy": round(-30 + 20 * u1, 1)}
