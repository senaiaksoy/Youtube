import { createHash, randomBytes, timingSafeEqual } from 'crypto';

const STATE_TTL_SECONDS = 10 * 60;

function hashState(state: string): string {
  return createHash('sha256').update(state).digest('hex');
}

export function createOAuthState() {
  const state = randomBytes(32).toString('hex');

  return {
    state,
    hashedState: hashState(state),
    maxAge: STATE_TTL_SECONDS,
  };
}

export function isValidOAuthState(state: string | null | undefined, hashedState: string | undefined) {
  if (!state || !hashedState) return false;

  const expected = Buffer.from(hashedState, 'hex');
  const actual = Buffer.from(hashState(state), 'hex');

  if (expected.length !== actual.length) return false;

  return timingSafeEqual(expected, actual);
}
