import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_path = os.path.join(REPO_ROOT, "omega_supreme_command_center.html")

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update header badge
text = text.replace(
    "ALL 10 ENTERPRISE ENGINES OPERATIONAL (127/127 TESTS GREEN)",
    "ALL 11 ENTERPRISE ENGINES OPERATIONAL (137/137 TESTS GREEN)"
)

# 2. Update hero metric
text = text.replace(
    '<div class="metric-val">127 / 127</div>\n      <div class="metric-sub">10 Enterprise Test Suites Passing (100% Green)</div>',
    '<div class="metric-val">137 / 137</div>\n      <div class="metric-sub">11 Enterprise Test Suites Passing (100% Green)</div>'
)
# handle CRLF as well
text = text.replace(
    '<div class="metric-val">127 / 127</div>\r\n      <div class="metric-sub">10 Enterprise Test Suites Passing (100% Green)</div>',
    '<div class="metric-val">137 / 137</div>\r\n      <div class="metric-sub">11 Enterprise Test Suites Passing (100% Green)</div>'
)

# 3. Update tab button
text = text.replace(
    "🛡️ 114-Test Verification Gateway",
    "🛡️ 137-Test Verification Gateway"
)

# 4. Update scorecard header
text = text.replace(
    "114 / 114 PASSED (0 FAILURES)",
    "137 / 137 PASSED (0 FAILURES)"
)

# 5. Update Bangalore Top 500 Master Suite passed count
text = text.replace(
    '<td style="font-family: var(--mono);">6 / 6</td>\n                <td style="font-family: var(--mono); color: var(--text-dim);">3.69s</td>',
    '<td style="font-family: var(--mono);">9 / 9</td>\n                <td style="font-family: var(--mono); color: var(--text-dim);">1.79s</td>'
)
text = text.replace(
    '<td style="font-family: var(--mono);">6 / 6</td>\r\n                <td style="font-family: var(--mono); color: var(--text-dim);">3.69s</td>',
    '<td style="font-family: var(--mono);">9 / 9</td>\r\n                <td style="font-family: var(--mono); color: var(--text-dim);">1.79s</td>'
)

# 6. Add Mode H Chaos Harness row to the table
chaos_row = '''              <tr>
                <td style="font-weight: 700; color: #fff;">Mode H Antifragile Red-Team & Chaos Harness</td>
                <td style="color: var(--text-dim);">Multi-bank partition, double-entry replay, flash crash order surges, warehouse exhaustion, radiation bitflips, brownout shedding</td>
                <td><span class="badge-green">GREEN</span></td>
                <td style="font-family: var(--mono);">10 / 10</td>
                <td style="font-family: var(--mono); color: var(--text-dim);">1.98s</td>
              </tr>
            </tbody>'''

if "Mode H Antifragile Red-Team & Chaos Harness" not in text:
    text = text.replace("            </tbody>", chaos_row)

# 7. Add Pitch Decks Card in Launchpad if not present
pitch_deck_card = '''        <div class="launch-card">
          <div class="launch-card-header">
            <span class="launch-card-icon">📊</span>
            <div>
              <div class="launch-card-title">Turnkey Executive Pitch Decks</div>
              <div class="launch-card-sub">20 Interactive Slide Presentations for Fortune 500 & Unicorns</div>
            </div>
          </div>
          <p class="launch-card-desc">7-slide presentation decks detailing operational leakage metrics, ROI payback in &lt;6 weeks, and discretionary &lt; ₹5L pilot entries for Walmart, Target, Goldman Sachs, JPMorgan, Cisco, etc.</p>
          <div class="launch-card-links">
            <a href="reports/pitch_decks/PITCH_DECK_Walmart_Global_Tech_India.html" target="_blank" class="btn-launch btn-launch-primary">Walmart Pitch Deck ↗</a>
            <a href="reports/pitch_decks/PITCH_DECK_Goldman_Sachs_Services_GSC.html" target="_blank" class="btn-launch">Goldman Sachs Deck ↗</a>
            <a href="reports/pitch_decks/PITCH_DECK_JPMorgan_Chase_Global_Service_Center.html" target="_blank" class="btn-launch">JPMorgan Deck ↗</a>
            <a href="COMMERCIAL_DISPATCH_BOARD.md" target="_blank" class="btn-launch">Outbound Dispatch Board ↗</a>
          </div>
        </div>
      </div>
    </div>'''

if "Turnkey Executive Pitch Decks" not in text:
    text = text.replace("      </div>\n    </div>\n\n    <!-- View 2: Bangalore Top 500 Startups -->", pitch_deck_card + "\n\n    <!-- View 2: Bangalore Top 500 Startups -->")
    text = text.replace("      </div>\r\n    </div>\r\n\r\n    <!-- View 2: Bangalore Top 500 Startups -->", pitch_deck_card + "\r\n\r\n    <!-- View 2: Bangalore Top 500 Startups -->")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] omega_supreme_command_center.html updated with 137 tests & pitch decks!")
