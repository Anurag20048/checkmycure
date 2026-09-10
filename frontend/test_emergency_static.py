from pathlib import Path

p = Path(__file__).with_name('emergency-sos.html')
s = p.read_text(encoding='utf-8')

assert '.emergency-container {\n            display: block;' in s
assert '.emergency-active {\n            display: none;' in s
assert '.emergency-active.active {\n            display: flex;' in s
# The hidden state must not be overridden by a second display:flex inside the same rule.
active_block = s.split('.emergency-active {', 1)[1].split('.emergency-active.active {', 1)[0]
assert active_block.count('display: flex;') == 0
assert 'onclick="activateEmergency()"' in s
assert 'SOS is intentionally user-triggered' in s
assert 'window.onload' not in s
assert 'DOMContentLoaded' not in s
print('Emergency static checks: PASS')
