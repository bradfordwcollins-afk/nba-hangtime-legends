# NBA Hangtime Legends

A heavily modded rebuild of Midway's **Maximum Hangtime** (Wolf Unit, TMS34010) with
legends-era rosters, new art, modern team colours and a pile of new game modes and options.
FBNeo driver name: **`nbamhtg`** (clone of `nbahangt`), 31 ROMs.

---

## Mod synopsis

### Rosters — "Legends" edition
Every team mixes its all-time greats with today's stars (3–5 players per team):

| Team | Players |
|------|---------|
| Atlanta | Trae Young, Dominique Wilkins, Mookie Blaylock, Kyle Korver |
| Boston | Larry Bird, Kevin McHale, Paul Pierce, Jayson Tatum, Robert Parish |
| Charlotte | Muggsy Bogues, Dell Curry, Larry Johnson, Glen Rice, Jamal Mashburn |
| Chicago | Michael Jordan, Scottie Pippen, Dennis Rodman, Derrick Rose, Steve Kerr |
| Cleveland | LeBron James, Kyrie Irving, Donovan Mitchell, Brad Daugherty |
| Dallas | Dirk Nowitzki, Luka Doncic, Michael Finley, Shawn Bradley |
| Denver | Nikola Jokic, Dikembe Mutombo, Jamal Murray, Carmelo Anthony, Chauncey Billups |
| Detroit | Isiah Thomas, Grant Hill, Joe Dumars, Bill Laimbeer, Ben Wallace |
| Golden State | Stephen Curry, Klay Thompson, Chris Mullin, Wilt Chamberlain |
| Houston | Hakeem Olajuwon, James Harden, Yao Ming, Tracy McGrady |
| Indiana | Reggie Miller, Tyrese Haliburton, Jalen Rose, Rik Smits, Ron Artest |
| LA Clippers | Chris Paul, Blake Griffin, Paul George, DeAndre Jordan |
| LA Lakers | Kobe Bryant, Magic Johnson, Pau Gasol, Kareem Abdul-Jabbar, James Worthy |
| Miami | Dwyane Wade, Alonzo Mourning, Tim Hardaway, Jimmy Butler, Bam Adebayo |
| Milwaukee | Giannis Antetokounmpo, Khris Middleton, Ray Allen, Glenn Robinson, Oscar Robertson |
| Minnesota | Kevin Garnett, Anthony Edwards, LaMelo Ball, Latrell Sprewell |
| New Jersey | Jason Kidd, Derrick Coleman, Kerry Kittles, Stephon Marbury |
| New York | Patrick Ewing, Jalen Brunson, Allan Houston, Walt Frazier |
| Orlando | Shaquille O'Neal, Penny Hardaway, Nick Anderson, Dwight Howard, Horace Grant |
| Philadelphia | Allen Iverson, Joel Embiid, Moses Malone, Julius Erving |
| Phoenix | Devin Booker, Charles Barkley, Steve Nash, Dan Majerle |
| Portland | Damian Lillard, Clyde Drexler, LaMarcus Aldridge, Arvydas Sabonis |
| Sacramento | Spud Webb, Vlade Divac, Mitch Richmond, DeMarcus Cousins |
| San Antonio | Tim Duncan, David Robinson, Tony Parker, Manu Ginobili, Victor Wembanyama |
| Seattle | Kevin Durant, Gary Payton, Russell Westbrook, Shawn Kemp, Shai Gilgeous-Alexander |
| Toronto | Vince Carter, Kawhi Leonard, Chris Bosh, DeMar DeRozan |
| Utah | Karl Malone, John Stockton, Jeff Hornacek, Pete Maravich |
| Vancouver | Ja Morant, Marc Gasol, Desmond Bane, Zach Randolph |
| Washington | Chris Webber, Anthony Davis, Juwan Howard, Bradley Beal |

- New in-game heads (photo-built, Jam heads re-used and re-skinned), skin tones matched head-to-body for every player.
- New mugshots for the new players, eyes and head sizes lined up with the 1996 mugs, jerseys cleaned up / recoloured.
- New nameplates, including full names (ANTETOKOUNMPO, ABDUL-JABBAR, GILGEOUS- / ALEXANDER).
- Prime / All-Star ratings for the original Hangtime players; ratings for every legend.
- Attract mode: "LEGENDS ROSTERS" and "HALL OF FAMERS" pages.
- Record mode: random opponent order, finishing with the title franchises.

### Teams, uniforms and courts
- 2025-26 team colours and home / away kits for every team, with a colour-clash check.
- **Jerseys follow the court**: whoever's court is picked wears home (outdoor = default).
- New select-screen logos for all 29 teams.
- Centre-court logos for every team; lanes and aprons coloured to match the jerseys, smoothed shading.
- Matchup-screen court choice: **Home / Away / Outdoor / Random** (team names shown).
  The Underground and Vortex courts were removed to free image ROM.

### Team Zone (new)
- A team meter that fills on assists, steals, blocks and alley-oops (x2).
- When full, **press COIN** to light Team Fire ("PRESS COIN" flashes under a full meter).
- Either team can light its fire, even while the other team is on fire.
- Team Fire countdown sits under the Team Zone bar.

### Super Maximum Settings menu (new options)
| Option | What it does |
|--------|--------------|
| **TEAM ZONE** | Turns the Team Zone meters on / off |
| **INJURY FIRE** | OFF, or 20–75 injuries given (FIRST TEAM or BOTH TEAMS): reach it and that team is on fire for the rest of the game (∞ in the countdown box) |
| **GAME RULES** | NBA RULES / BLOCK PARTY / TRIPLE THREAT / OOP CITY / DUNKFEST / RANDOM |
| **NO GOALTENDING** | Goaltending is never called — every swat is a block |
| **FATALITY PUSHES** | On-fire pushers can send players flying in flames |
| **UNLIMITED TURBO**, fast passing, hyper speed | Also on the DIP switches |
| Matchup codes | Codes selectable from the menu |

**Game rules**
- **NBA Rules** — normal scoring.
- **Block Party** — every block takes a point off the blocked team (never below 0).
- **Triple Threat** — made 3s are worth 3, every other basket 1.
- **Oop City** — alley-oops are worth 3, double dunks 4.
- **Dunkfest** — dunks are worth 3, every other basket 1.
- **Random** — picked per game on the versus screen with a roulette (Dunkfest is the rarest).
  The rule set shows on the versus screen, at the opening tip and on the in-game scoreboard plate.

**Opening the menu**: press **START + COIN** together on the attract screens or the CHOOSE OPTION menu.
Leaving it returns joined players to the CHOOSE OPTION menu (their credits are refunded and re-taken).

### New stats
- **Injuries given**: pushes that injure an opponent. The halftime / final stats INJURED row reads taken / given (INJ T/G).

### Fixes and polish
- 2-player cabinet: player 2 can activate Team Zone.
- Fatality-push fire palette glitch fixed; fatality pushes only by an on-fire pusher.
- DCS "call 0" sound cut-out fixed.
- Garbled select-screen mugs / logos fixed; shatter peeker head removed.
- "Winner stays on free" message removed from the CHOOSE OPTION screen.
- Title screen SUPER / LEGENDS.

### DIP switches (FBNeo `nbamhtg`)
Fatality Pushes, Unlimited Turbo, Fast Passing, Hyper Speed, Team Zone, plus the original cabinet / coinage switches.

---

## Requirements

- **DOSBox** 0.74-3 (or compatible) — runs the legacy DOS assembler, linker (`bigsrec`), and graphics processor (`loadw`)
- **Python 3** — orchestrates the build pipeline
- **GNU Make** (`gmake`) — included in `TOOLS/` for DOS; invoked inside DOSBox

## Step-by-Step Build

```bash
# 1. Process graphics  (palettes, sprite tables, GFX ROMs)
cd BACKUP/XCODE101L
python3 buildgfx.py

# 2. Compile code & link program ROMs
python3 build.py

# 3. All outputs are in:
#    IMG/rom/  — GFX byte-plane ROMs
#    ROM/      — program ROMs (u54/u63, 512 KB each)
```

## FBNeo

`FBNEO/d_wunit.cpp` is the Wolf Unit driver with the **`nbamhtg`** set (ROM list, CRCs and DIP switches);
`FBNEO/nbamhtg_entry.txt` is just that entry. Build the ROMs, put them in `nbamhtg.zip`, and use this driver.
The CRCs in the driver match the current build.

## Structure

| Directory | Contents |
|-----------|----------|
| `BACKUP/XCODE101L/` | Main build directory — source, build scripts, tools |
| `BACKUP/XCODE101L/IMG/` | Graphics assets, MISC.LOD, court data |
| `BACKUP/XCODE101L/ROM/` | Program ROM linker output |
| `BACKUP/XCODE101L/TOOLS/` | DOS toolchain (gmake, bigsrec, loadw, vidram) |
| `FBNEO/` | FBNeo driver for the `nbamhtg` set |
| `SRC/` | Assembly source files |
| `IMG/` | Root-level graphics workspace |
| `DOC/` | Technical documentation |

Based on the NBA Hangtime rebuild by Asure.
