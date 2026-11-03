# Poligent

Tracks German federal labor-law legislation while it is still in progress, and tells a person whether a given piece of legislation may affect their situation. Terms are in English. Where a term corresponds to a DIP concept, the German DIP name is listed as its alias.

## Legislative process

**Procedure** (DIP: _Vorgang_):
One legislative procedure in the Bundestag, such as a single bill, from introduction to its final outcome.
_Avoid_: Initiative (in DIP, this means who introduced a bill), bill, law (a Procedure is not yet a law)

**Procedure step** (DIP: _Vorgangsposition_):
One step in a Procedure's history with a date, such as a first reading, a committee referral, a vote or a promulgation.
_Avoid_: Event, status entry

**Printed paper** (DIP: _Drucksache_):
An official document of the Bundestag or Bundesrat that belongs to a Procedure. It is an official work (amtliches Werk): we may quote it briefly with a source, but never alter it.
_Avoid_: Document, PDF

**Key document**:
A Printed paper whose full text we analyse for a Procedure: its Bill or its Committee recommendation.
_Avoid_: Main document

**Bill** (DIP: _Gesetzentwurf_):
The Printed paper that contains the proposed law text of a Procedure.
_Avoid_: Draft, proposal

**Committee recommendation** (DIP: _Beschlussempfehlung und Bericht_):
The Printed paper in which the responsible committee recommends how the Bundestag should vote, often with an amended law text.
_Avoid_: Report

**DIP status** (DIP: _Beratungsstand_):
DIP's own free-text label for where a Procedure currently stands. It is raw source data and is never shown to the user without being mapped to a Legislative state first.
_Avoid_: Status (ambiguous with Legislative state)

**Legislative state**:
Our own small, stable classification of where a Procedure stands: `INTRODUCED`, `IN_DELIBERATION`, `DECISION_READY`, `PASSED`, `ENACTED`, `FAILED` or `UNKNOWN`. It sets how strongly an answer must warn that the outcome is still open. `UNKNOWN` means we could not classify the DIP status, and it carries the strongest warning.
_Avoid_: Status, stage, phase

**Enacted**:
The Legislative state of a Procedure whose law has been promulgated. It says nothing about when the law takes effect, which can differ between its articles (see Entry into force).
_Avoid_: In force, valid

**Entry into force** (DIP: _Inkrafttreten_):
The date on which some or all of an enacted law starts to apply. One law can have several.
_Avoid_: Effective date, validity

**Status change**:
The appearance of a new Procedure step for a Procedure we track.
_Avoid_: Update, change

**Electoral term** (DIP: _Wahlperiode_):
One term of the Bundestag. When a term ends, every unfinished Procedure lapses.
_Avoid_: Legislative period, session

**Lapse** (DIP: _Diskontinuität_):
The ending of every unfinished Procedure at the end of an Electoral term. A lapsed Procedure is `FAILED`.
_Avoid_: Expiry

**Labor-law procedure**:
A Procedure of type Gesetzgebung in the current Electoral term that DIP files under a labor-related Sachgebiet or deskriptor. Only these are tracked.
_Avoid_: Relevant procedure (relevance is per person, see Relevance assessment)

## Personal relevance

**Profile**:
The few facts about a person's situation that we use to judge relevance: exactly one Employment status plus any number of Circumstances. A Profile is not an account.
_Avoid_: User, account, persona

**Employment status**:
A person's single role in working life: employee, self-employed/freelancer, apprentice, civil servant or employer.
_Avoid_: Job type, role

**Circumstance**:
A situation that can apply alongside any Employment status: parent or caring for relatives, shift or night work, part-time or mini-job.
_Avoid_: Flag, tag, attribute

**Relevance assessment**:
A grounded judgement of whether a Procedure may affect someone with a given Profile. It consists of a Verdict, its reasoning, and the passages it cites.
_Avoid_: Relevance score, match, confidence

**Verdict**:
The outcome of a Relevance assessment: relevant, possibly relevant or not relevant. A Verdict without a cited passage can be at most "possibly relevant".
_Avoid_: Score, rating
