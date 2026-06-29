from __future__ import annotations


def _claims_for(text: str) -> list[dict[str, str]]:
    from pipeline.step_009_canonical_claims import extract_canonical_claims_from_payload

    payload = {
        "raw_text": text,
        "preprocessed_text": text,
        "source_text_id": "src-canon-prep-001",
        "metadata": {"source": {"kind": "string"}},
        "operations_applied": [],
        "sentences": [
            {"sentence_id": "sent-0001", "text": text, "index": 0, "start_offset": 0, "end_offset": len(text)},
        ],
    }
    result = extract_canonical_claims_from_payload(payload, {"emit_semantic_claims": True})
    return result["semantic_claims"]["claims"]


# UC-009 MF-4 | FUN-CANON-004 AC-1 | BR-REL-PREP-ROUTE-001 | TASK-PIZZA-RED-002 | TB-CANON-001
def test_canonical_claims_project_from_to_route_as_relations_not_compound_class():
    claims = _claims_for("Luigi rides from Harbor Market to Pine Street, passes the public library, and reaches Central Cafe at 12:18 p.m.")
    statements = {claim["statement"] for claim in claims}
    objects = {claim.get("object", "") for claim in claims}

    assert "Luigi rides_from HarborMarket" in statements
    assert "Luigi rides_to PineStreet" in statements
    assert "Luigi passes PublicLibrary" in statements
    assert "Luigi reaches CentralCafe" in statements
    assert "HarborMarketToPineStreet" not in objects
    assert "CentralCafeAt1218PM" not in objects


# UC-009 MF-4 | FUN-CANON-004 AC-2 | BR-CANON-CONTEXT-OBJECT-001 | TASK-PIZZA-RED-002 | TB-CANON-002
def test_canonical_claims_strip_contextual_prepositional_tails_from_objects():
    claims = _claims_for("Luigi Bianchi manages delivery orders for Mario's Pizzeria.") + _claims_for("Luca grates aged parmesan over the edge.")
    statements = {claim["statement"] for claim in claims}
    objects = {claim.get("object", "") for claim in claims}

    assert "LuigiBianchi manages DeliveryOrder" in statements
    assert "Luca grates AgedParmesan" in statements
    assert "DeliveryOrderForMarioSPizzeria" not in objects
    assert "AgedParmesanOverTheEdge" not in objects


# UC-009 MF-4 | FUN-CANON-004 AC-3 | BR-CANON-LIST-OBJECT-001 | TASK-PIZZA-RED-003 | TB-CANON-003
def test_canonical_claims_split_list_objects_before_contextual_tail():
    claims = _claims_for("The tablet links Mario's Pizzeria, Luigi Bianchi, Central Cafe, Nina Patel, order CAFE-17, and the Vesuvio pie in the same delivery record.")
    statements = {claim["statement"] for claim in claims}
    objects = {claim.get("object", "") for claim in claims}

    assert {
        "Tablet links MarioSPizzeria",
        "Tablet links LuigiBianchi",
        "Tablet links CentralCafe",
        "Tablet links NinaPatel",
        "Tablet links OrderCAFE17",
        "Tablet links VesuvioPie",
    } <= statements
    assert "MarioSPizzeriaLuigiBianchiCentralCafeNinaPatelOrderCAFE17AndTheVesuvioPie" not in objects
    assert "VesuvioPieInTheSameDeliveryRecord" not in objects


# UC-009 MF-4 | FUN-CANON-004 AC-4 | BR-CANON-REPORTING-THAT-001 | TASK-PIZZA-RED-004 | TB-CANON-004
def test_canonical_claims_decompose_reporting_that_clauses_without_that_predicate():
    claims = _claims_for("Nina tells Luigi that the basil aroma matches the request, and Luigi records the delivery as completed.")
    statements = {claim["statement"] for claim in claims}
    predicates = {claim.get("predicate", "") for claim in claims}
    objects = {claim.get("object", "") for claim in claims}

    assert "Nina tells Luigi" in statements
    assert "BasilAroma matches Request" in statements
    assert "Luigi records Delivery" in statements
    assert "thes" not in predicates
    assert "BasilAromaMatchTheRequest" not in objects
    assert "LuigiRecordTheDeliveryAsCompleted" not in objects
