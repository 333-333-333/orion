from __future__ import annotations

from pathlib import Path

import pytest

from observability import JsonlFileLogSink
from orion import ORION


_PARAGRAPH_DIR = Path(__file__).parent / "fixtures" / "infosec_3k_paragraphs"


_CASES = [
    ("p001", "information security;information asset;confidential document;source code repository", "", ""),
    ("p002", "confidentiality;integrity;availability;CIA triad", "", ""),
    ("p003", "security policy;security standard;security procedure;security baseline", "", ""),
    ("p004", "board of directors;information security manager;asset owner;security analyst;auditor", "", ""),
    ("p005", "risk management;risk;threat;vulnerability;asset", "", ""),
    ("p006", "preventive control;detective control;corrective control;compensating control", "", ""),
    ("p007", "public information;internal information;confidential information;restricted information;personal data;financial data;authentication data", "", ""),
    ("p008", "access control;identification;authentication;authorization;accountability;user account", "", ""),
    ("p009", "credential;password;certificate;access token;API key;private key;compromised credential", "", ""),
    ("p010", "multi-factor authentication;knowledge factor;possession factor;inherence factor;password;hardware token;mobile authenticator application;fingerprint;unauthorized access", "authentication|reduce|risk;password|be|factor;fingerprint|be|factor", "password|knowledge;fingerprint|inherence;token|possession;application|possession;factor|type"),
    ("p011", "least privilege;permission;role;user group;excessive permission;dormant account access;orphaned account access", "", ""),
    ("p012", "identity and access management;user provisioning;user deprovisioning;access certification;joiner process;leaver process;identity management system;access management system", "", ""),
    ("p013", "network security;firewall;network access control system;intrusion detection system;intrusion prevention system;virtual private network;demilitarized zone;production network", "", ""),
    ("p014", "endpoint security;antivirus software;endpoint detection and response;device encryption;patch management;configuration hardening;laptop", "", ""),
    ("p015", "application security;software vulnerability;input validation;output encoding;secure session management;code review", "", ""),
    ("p016", "web application;mobile application;API;database server;load balancer;API gateway;content delivery network", "", ""),
    ("p017", "cloud security;cloud account;cloud workload;virtual machine;object storage bucket;cloud access security broker;cloud security posture management tool", "", ""),
    ("p018", "cryptography;encryption;decryption;cryptographic key;symmetric encryption;asymmetric encryption;digital signature;hash function", "", ""),
    ("p019", "key management;key generation;key storage;key rotation;key revocation;hardware security module;key management service", "", ""),
    ("p020", "logging and monitoring;log record;audit log;security alert;security incident;false positive;false negative", "", ""),
    ("p021", "security information and event management system;log collection;log normalization;log correlation;detection rule;log retention policy", "", ""),
    ("p022", "incident response;preparation;analysis;containment;recovery;incident response plan", "", ""),
    ("p023", "malware infection;phishing attack;ransomware attack;data breach;denial-of-service attack;unauthorized access;insider misuse;lost device incident", "", ""),
    ("p024", "business continuity;disaster recovery;business impact analysis;recovery time objective;recovery point objective;backup policy;disaster recovery test", "", ""),
    ("p025", "supplier security;cloud provider;managed service provider;software vendor;contract;data processing agreement;service-level agreement;third-party access", "", ""),
    ("p026", "physical security;data center;badge reader;security camera;locked cabinet;environmental controls;restricted areas", "", ""),
    ("p027", "human resource security;background check;confidentiality agreement;security awareness training;termination procedure;acceptable use policies", "", ""),
    ("p028", "security awareness;phishing awareness;password awareness;data handling awareness;remote work awareness;simulated phishing exercises", "", ""),
    ("p029", "compliance;compliance requirement;legal requirement;regulatory requirement;contractual requirement;corrective action", "", ""),
    ("p030", "privacy;data subject;data controller;data processor;privacy notice;data deletion", "", ""),
    ("p031", "data lifecycle management;data creation;data storage;data processing;data disposal;data classification", "", ""),
    ("p032", "change management;change request;normal change;emergency change;change rollback;unauthorized change", "", ""),
    ("p033", "vulnerability management;vulnerability scan;vulnerability finding;remediation;mitigation;vulnerability exceptions", "", ""),
    ("p034", "threat intelligence;threat actor;cybercriminal group;indicator of compromise;tactic;technique", "", ""),
    ("p035", "secure architecture;defense in depth;zero trust;network segmentation;strong authentication;encryption;backup and recovery", "", ""),
    ("p036", "security control;asset;risk;threat;vulnerability;requirement;incident", "", ""),
    ("p037", "customer database;personal data;database server;production network;firewall;security analyst;restricted information", "", ""),
    ("p038", "remote access;remote employee;laptop;corporate application;multi-factor authentication;virtual private network;endpoint detection and response", "", ""),
    ("p039", "phishing scenario;threat actor;malicious link;compromised credential;cloud account;email filtering;incident response", "", ""),
    ("p040", "ransomware scenario;malware;file server;availability;network segmentation;backup restoration;incident response team;corrective actions", "", ""),
    ("p041", "data breach scenario;access control;restricted document repository;confidential information;personal data;security alert;privacy officer;regulatory obligations", "", ""),
    ("p042", "ORION;security concepts;hierarchical relationships;meaningful relationships;information asset;security control;security incident;authentication factor;threat actor;compliance requirement;cloud workload;endpoint;supplier", "", ""),
    ("p043", "users;systems;roles;permissions;controls;risks;threats;vulnerabilities;incidents;assets;policies;requirements;suppliers;auditors;encryption;backups;logging;monitoring", "user|access|system;role|include|permission;control|reduce|risk;threat|exploit|vulnerability;incident|affect|asset", ""),
]


def _split(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(";") if item.strip()]


def _split_relations(raw: str) -> list[tuple[str, str, str]]:
    relations = []
    for item in _split(raw):
        subj, pred, obj = [piece.strip() for piece in item.split("|")]
        relations.append((subj, pred, obj))
    return relations


def _concept_texts(result: dict) -> list[str]:
    return [str(item.get("text", "")).strip() for item in result.get("concepts", []) if isinstance(item, dict)]


def _relation_texts(result: dict) -> list[tuple[str, str, str]]:
    return [
        (
            str(item.get("subject_text", "")).strip(),
            str(item.get("predicate", "")).strip(),
            str(item.get("object_text", "")).strip(),
        )
        for item in result.get("relations", [])
        if isinstance(item, dict)
    ]


def _taxonomy_texts(result: dict) -> list[tuple[str, str]]:
    return [
        (
            str(item.get("subclass", "")).strip(),
            str(item.get("superclass", "")).strip(),
        )
        for item in result.get("taxonomy_relations", [])
        if isinstance(item, dict)
    ]


def _has_phrase(texts: list[str], phrase: str) -> bool:
    wanted = phrase.lower()
    return any(wanted in text.lower() for text in texts)


def _has_relation(texts: list[tuple[str, str, str]], expected: tuple[str, str, str]) -> bool:
    subj, pred, obj = expected
    subj = subj.lower()
    pred = pred.lower()
    obj = obj.lower()
    return any(
        subj in actual_subj.lower()
        and pred == actual_pred.lower()
        and obj in actual_obj.lower()
        for actual_subj, actual_pred, actual_obj in texts
    )


def _has_taxonomy(texts: list[tuple[str, str]], expected: tuple[str, str]) -> bool:
    subclass, superclass = expected
    subclass = subclass.lower()
    superclass = superclass.lower()
    return any(
        subclass in actual_subclass.lower()
        and superclass in actual_superclass.lower()
        for actual_subclass, actual_superclass in texts
    )


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case[0])
def test_infosec_paragraph_semantics(case, tmp_path):
    paragraph_id, expected_concepts_raw, expected_relations_raw, expected_taxonomies_raw = case
    paragraph_path = _PARAGRAPH_DIR / f"{paragraph_id}.txt"
    text = paragraph_path.read_text(encoding="utf-8").strip()
    assert text, f"paragraph empty: {paragraph_path.name}"

    runtime_log = tmp_path / f"{paragraph_id}-runtime-events.jsonl"
    sut = ORION(config={"logging": {"sink": JsonlFileLogSink(runtime_log)}, "spacy_model": "en_core_web_lg", "output_strategy": "rdf"})
    result = sut.process(text)

    output = result.get("output", {})
    graph = output.get("graph", {}) if isinstance(output, dict) else {}
    concepts = _concept_texts(result)
    relations = _relation_texts(result)
    taxonomies = _taxonomy_texts(result)

    assert output.get("strategy") == "rdf"
    assert graph, f"graph missing for {paragraph_path.name}"
    assert concepts, f"concepts missing for {paragraph_path.name}"
    assert graph.get("schema", {}).get("classes"), f"schema.classes missing for {paragraph_path.name}"

    for expected in _split(expected_concepts_raw):
        assert _has_phrase(concepts, expected), f"{paragraph_path.name}: missing concept '{expected}'"

    for expected in _split_relations(expected_relations_raw):
        assert _has_relation(relations, expected), f"{paragraph_path.name}: missing relation {expected}"

    for expected in [tuple(item.split("|")) for item in _split(expected_taxonomies_raw)]:
        assert _has_taxonomy(taxonomies, expected), f"{paragraph_path.name}: missing taxonomy {expected}"
