import hashlib
import uuid
import json
import ecc.Key as Key_Module

Key = Key_Module.Key

class Node:
    def __init__(self, payload={}, edges=[], id=id):
        if id is None:
            id = uuid.uuid4()

        self.creds = Key.generate(521)
        self.payload_sig = None
        self.payload = None
        self.set_payload(payload)
        self.edges = None
        self.edges_sig = None
        self.set_edges(edges)
        self.id = id
        self.seed = None

    def set_payload(self, payload):
        json_msg = json.dumps(payload, sort_keys=True)
        sig = self.creds.sign(json_msg)
        self.payload_sig = sig

    def set_edges(self, edges):
        self.edge_sigs = None
        self.edges = None
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        new_json = json.dumps({"head": edge.__dict__, "tail": self.edge_sigs}, sort_keys=True)
        sig = self.creds.sign(new_json)
        self.edge_sigs = sig

    def __add__(self, other):
        self.link(other)

    def link(self, other, rel=None):
        if not isinstance(other, NodeSig):
            assert TypeError("May only link/add to Node Signatures")
        edge = Edge(self, other, rel)
        self.edges.append(edge)
        other.edges.append(edge)

    def to_hash(self):
        pass

class NodeSig:
    def __init__(self, payload_sig, creds):
        self.payload_sig = payload_sig
        self.creds = creds

    def validate(self, node):
        payload_sig = hashlib.sha256(json.dumps(node.payload, sort_keys=True))
        if not payload_sig == self.payload_sig:
            assert ValueError("Invalid payload")


class Edge:
    default_relation = {"type":None, "directional":False}
    def __init__(self, obj, sub, rel=None, id=None):
        if id is None:
            id = uuid.uuid4()
        if rel is None:
            rel = Edge.default_relation
        self.rel = rel
        self.obj = obj
        self.sub = sub
        self.id = id
    
    def to_hash(self, ref_node):
        hash_func = hashlib.sha256()


'''
hash(node, stack=()):
    h_payload = hash(node.payload)
    for edge in edges:
        if node is edge.obj:
            h_edge_payloads = hash(h_payload, guid, hash(edge.sub.payload))
        else:
            h_edge_payloads = hash(hash(edge.obj.payload), guid, h_payload)
        

'''