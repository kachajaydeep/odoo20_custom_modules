Steps to Make Passes Available to Real Users
1️⃣ Complete Class Review

    1. Go to Google Wallet API console.
    2. Ensure your loyalty class is in production (review approved).
    3. Set reviewStatus: "UNDER_REVIEW" → reviewStatus: "APPROVED" once Google approves it.

2️⃣ Switch from Test Issuer to Production Issuer

    1. Every Google Wallet class has an issuerId.
    2. Test issuer IDs start with TEST_.
    3. To issue passes to real users, you need a real issuer ID.

3️⃣ Verify Object Creation

    1. When creating the object, the classId must point to the approved class.
    2. The object should not be in test mode.