import os
import time

import msal
import requests
from dotenv import load_dotenv


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"

TARGET_USER_UPN = (
    "jordan.reyes@AetherisOrbitalDynamics.onmicrosoft.com"
)

# Only explicitly approved assigned groups may be removed.
OFFBOARDING_MANAGED_GROUPS = {
    "Aetheris-Mission-Control-Operators"
}

VERIFICATION_ATTEMPTS = 3
VERIFICATION_DELAY_SECONDS = 2


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

def get_access_token():
    authority = (
        f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    app = msal.ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET,
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in result:
        raise RuntimeError(
            "Authentication failed: "
            + result.get(
                "error_description",
                result.get("error", "Unknown error"),
            )
        )

    return result["access_token"]


# ---------------------------------------------------------
# Microsoft Graph read operations
# ---------------------------------------------------------

def get_user(headers, user_upn):
    response = requests.get(
        f"{GRAPH_BASE_URL}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName,accountEnabled",
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Unable to retrieve user. "
            f"HTTP {response.status_code}: {response.text}"
        )

    return response.json()


def get_memberships(headers, user_id):
    response = requests.get(
        f"{GRAPH_BASE_URL}/users/{user_id}/memberOf",
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Unable to retrieve memberships. "
            f"HTTP {response.status_code}: {response.text}"
        )

    return response.json()["value"]


# ---------------------------------------------------------
# Offboarding actions
# ---------------------------------------------------------

def disable_account(headers, user):
    print("\nOFFBOARDING ACTION 1 - DISABLE ACCOUNT")

    if user["accountEnabled"] is False:
        print("SKIPPED: Account is already disabled.")
        return

    start_time = time.perf_counter()

    response = requests.patch(
        f"{GRAPH_BASE_URL}/users/{user['id']}",
        headers=headers,
        json={"accountEnabled": False},
        timeout=30,
    )

    elapsed_time = time.perf_counter() - start_time

    if response.status_code != 204:
        raise RuntimeError(
            f"Account disable failed. "
            f"HTTP {response.status_code}: {response.text}"
        )

    print("SUCCESS: Account disable request completed.")
    print(
        f"Graph API execution time: {elapsed_time:.3f} seconds"
    )


def revoke_sessions(headers, user_id):
    print("\nOFFBOARDING ACTION 2 - REVOKE SESSIONS")

    start_time = time.perf_counter()

    response = requests.post(
        f"{GRAPH_BASE_URL}/users/"
        f"{user_id}/revokeSignInSessions",
        headers=headers,
        timeout=30,
    )

    elapsed_time = time.perf_counter() - start_time

    if response.status_code != 200:
        raise RuntimeError(
            f"Session revocation failed. "
            f"HTTP {response.status_code}: {response.text}"
        )

    result = response.json()

    if result.get("value") is not True:
        raise RuntimeError(
            "Microsoft Graph did not confirm the "
            "session revocation request."
        )

    print("SUCCESS: Session revocation request completed.")
    print(
        f"Graph API execution time: {elapsed_time:.3f} seconds"
    )


def verify_group_removed(
    headers,
    user_id,
    group_name,
):
    for attempt in range(
        1,
        VERIFICATION_ATTEMPTS + 1,
    ):
        memberships = get_memberships(
            headers,
            user_id,
        )

        current_group_names = {
            membership.get("displayName")
            for membership in memberships
        }

        if group_name not in current_group_names:
            print(
                f"VERIFIED: {group_name} is no longer "
                f"assigned to the user."
            )
            return True

        if attempt < VERIFICATION_ATTEMPTS:
            print(
                f"Verification attempt {attempt}: "
                f"{group_name} is still visible."
            )
            print(
                f"Waiting {VERIFICATION_DELAY_SECONDS} "
                f"seconds before retry..."
            )

            time.sleep(
                VERIFICATION_DELAY_SECONDS
            )

    print(
        f"WARNING: {group_name} remained visible after "
        f"{VERIFICATION_ATTEMPTS} verification attempts."
    )

    return False


def remove_managed_access(
    headers,
    user_id,
    memberships,
):
    print(
        "\nOFFBOARDING ACTION 3 - "
        "REMOVE MANAGED ASSIGNED ACCESS"
    )

    removable_groups = []

    for membership in memberships:
        group_name = membership.get(
            "displayName",
            "Unknown",
        )

        group_id = membership.get("id")
        group_types = membership.get(
            "groupTypes",
            [],
        )

        # Dynamic memberships are controlled by
        # directory attributes and group rules.
        if "DynamicMembership" in group_types:
            print(
                f"SKIPPED: {group_name} "
                f"- dynamic membership"
            )
            continue

        # Assigned groups outside the allowlist
        # are intentionally left untouched.
        if group_name not in OFFBOARDING_MANAGED_GROUPS:
            print(
                f"SKIPPED: {group_name} "
                f"- not in offboarding allowlist"
            )
            continue

        if not group_id:
            print(
                f"SKIPPED: {group_name} "
                f"- group ID unavailable"
            )
            continue

        removable_groups.append(
            {
                "name": group_name,
                "id": group_id,
            }
        )

    if not removable_groups:
        print(
            "No allowlisted assigned access "
            "requires removal."
        )

        for group_name in OFFBOARDING_MANAGED_GROUPS:
            verify_group_removed(
                headers,
                user_id,
                group_name,
            )

        return

    for group in removable_groups:
        group_name = group["name"]
        group_id = group["id"]

        print(
            f"Removing assigned access: "
            f"{group_name}..."
        )

        start_time = time.perf_counter()

        response = requests.delete(
            f"{GRAPH_BASE_URL}/groups/"
            f"{group_id}/members/"
            f"{user_id}/$ref",
            headers=headers,
            timeout=30,
        )

        elapsed_time = (
            time.perf_counter() - start_time
        )

        if response.status_code != 204:
            raise RuntimeError(
                f"Group removal failed for "
                f"{group_name}. "
                f"HTTP {response.status_code}: "
                f"{response.text}"
            )

        print(
            f"SUCCESS: Removal request completed "
            f"for {group_name}."
        )
        print(
            f"Graph API execution time: "
            f"{elapsed_time:.3f} seconds"
        )

        verify_group_removed(
            headers,
            user_id,
            group_name,
        )


# ---------------------------------------------------------
# Reporting
# ---------------------------------------------------------

def print_access_discovery(memberships):
    print("\nACCESS DISCOVERY AND CLASSIFICATION")

    if not memberships:
        print("No direct group memberships returned.")
        return

    for membership in memberships:
        group_name = membership.get(
            "displayName",
            "Unknown",
        )

        group_types = membership.get(
            "groupTypes",
            [],
        )

        print(f"\nGroup: {group_name}")

        if "DynamicMembership" in group_types:
            print("Membership type: Dynamic")
            print(
                "Decision: SKIP - "
                "attribute-driven membership"
            )

        elif group_name in OFFBOARDING_MANAGED_GROUPS:
            print("Membership type: Assigned")
            print(
                "Decision: APPROVED for "
                "offboarding-managed removal"
            )

        else:
            print("Membership type: Assigned")
            print(
                "Decision: SKIP - "
                "not in offboarding allowlist"
            )


def print_final_state(
    headers,
    user_id,
    user_upn,
):
    user = get_user(
        headers,
        user_upn,
    )

    memberships = get_memberships(
        headers,
        user_id,
    )

    print("\nFINAL IDENTITY STATE")
    print(
        "Account enabled:",
        user["accountEnabled"],
    )

    print("\nFINAL ACCESS STATE")

    if not memberships:
        print("No direct group memberships returned.")

    for membership in memberships:
        group_name = membership.get(
            "displayName",
            "Unknown",
        )

        group_types = membership.get(
            "groupTypes",
            [],
        )

        if "DynamicMembership" in group_types:
            group_type = "Dynamic"
        else:
            group_type = "Assigned"

        print(
            f"- {group_name} ({group_type})"
        )


# ---------------------------------------------------------
# Main workflow
# ---------------------------------------------------------

def main():
    print(
        "AETHERIS ORBITAL DYNAMICS "
        "- AUTOMATED OFFBOARDING"
    )

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    print("Authentication successful.")
    print(
        "Microsoft Graph access token acquired."
    )

    user = get_user(
        headers,
        TARGET_USER_UPN,
    )

    print("\nTARGET IDENTITY")
    print("Display name:", user["displayName"])
    print(
        "User principal name:",
        user["userPrincipalName"],
    )
    print(
        "Account enabled:",
        user["accountEnabled"],
    )

    memberships = get_memberships(
        headers,
        user["id"],
    )

    print_access_discovery(
        memberships
    )

    disable_account(
        headers,
        user,
    )

    revoke_sessions(
        headers,
        user["id"],
    )

    remove_managed_access(
        headers,
        user["id"],
        memberships,
    )

    print_final_state(
        headers,
        user["id"],
        TARGET_USER_UPN,
    )

    print("\nOFFBOARDING WORKFLOW COMPLETE")


if __name__ == "__main__":
    try:
        main()

    except requests.RequestException as error:
        print(
            "\nNETWORK ERROR:",
            error,
        )

    except RuntimeError as error:
        print(
            "\nWORKFLOW ERROR:",
            error,
        )