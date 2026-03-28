from dataclasses import dataclass, field


class ASTNode:
    pass


@dataclass
class MemberNode(ASTNode):
    modifier: str
    type_:    str
    name:     str
    line:     int


@dataclass
class ClassNode(ASTNode):
    name:    str
    members: list[MemberNode] = field(default_factory=list)
    line:    int = 0

    def __repr__(self):
        members_repr = "\n  ".join(repr(m) for m in self.members)
        return (
            f"ClassNode(name='{self.name}', line={self.line}, members=[\n"
            f"  {members_repr}\n])"
        )
