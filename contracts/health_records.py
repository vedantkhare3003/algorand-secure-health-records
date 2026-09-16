from algopy import ARC4Contract, Account, Bytes, BoxMap, Txn, UInt64, arc4


class HealthRecordsContract(ARC4Contract):
    """
    Secure Health Records access-control smart contract.

    The contract stores:
    - ownership of a health record
    - cryptographic hash of the record
    - patient/provider access permissions

    Actual medical files remain off-chain.
    """

    def __init__(self) -> None:
        # record_id -> patient account
        self.record_owner = BoxMap(
            Bytes,
            Account,
            key_prefix=b"owner_",
        )

        # record_id -> cryptographic hash
        self.record_hash = BoxMap(
            Bytes,
            Bytes,
            key_prefix=b"hash_",
        )

        # record_id + provider address -> access status
        self.access = BoxMap(
            Bytes,
            UInt64,
            key_prefix=b"access_",
        )

    @arc4.abimethod
    def register_record(
        self,
        record_id: Bytes,
        record_hash: Bytes,
    ) -> None:
        """
        Register a new healthcare record.

        The caller becomes the owner of the record.
        """

        assert record_id not in self.record_owner, "Record already exists"
        assert record_hash, "Record hash cannot be empty"

        self.record_owner[record_id] = Txn.sender
        self.record_hash[record_id] = record_hash

    @arc4.abimethod
    def grant_access(
        self,
        record_id: Bytes,
        provider: Account,
    ) -> None:
        """
        Grant a healthcare provider access to a record.
        """

        assert record_id in self.record_owner, "Record does not exist"
        assert (
            Txn.sender == self.record_owner[record_id]
        ), "Only the patient can grant access"

        access_key = record_id + provider.bytes

        self.access[access_key] = UInt64(1)

    @arc4.abimethod
    def revoke_access(
        self,
        record_id: Bytes,
        provider: Account,
    ) -> None:
        """
        Revoke a healthcare provider's access to a record.
        """

        assert record_id in self.record_owner, "Record does not exist"
        assert (
            Txn.sender == self.record_owner[record_id]
        ), "Only the patient can revoke access"

        access_key = record_id + provider.bytes

        self.access[access_key] = UInt64(0)

    @arc4.abimethod
    def has_access(
        self,
        record_id: Bytes,
        provider: Account,
    ) -> UInt64:
        """
        Return 1 if the provider has access, otherwise 0.
        """

        assert record_id in self.record_owner, "Record does not exist"

        access_key = record_id + provider.bytes

        if access_key in self.access:
            return self.access[access_key]

        return UInt64(0)

    @arc4.abimethod
    def get_record_hash(
        self,
        record_id: Bytes,
    ) -> Bytes:
        """
        Return the stored cryptographic hash of a record.
        """

        assert record_id in self.record_owner, "Record does not exist"

        return self.record_hash[record_id]

    @arc4.abimethod
    def get_record_owner(
        self,
        record_id: Bytes,
    ) -> Account:
        """
        Return the patient account that owns the record.
        """

        assert record_id in self.record_owner, "Record does not exist"

        return self.record_owner[record_id]