import logging

from services.cloudflare import updatePublicKey, updateLicenseKey
from services.common import getCurrentAccount
from utils.wireguard import generateWireguardKeys


def resetAccountKey(logger=logging.Logger(__name__)):
    """
    Reset account private key, and update public key to Cloudflare
    :param logger:
    :return:
    """
    # Get current account
    account = getCurrentAccount(logger)
    logger.info(f"Reset account key for account: {account.account_id}")

    # Generate new keys
    privkey, pubkey = generateWireguardKeys()
    updatePublicKey(account, pubkey)
    logger.info(f"New public key: {pubkey}")
    logger.info(f"New private key: {privkey}")

    # Save new private key
    account.private_key = privkey
    # Save account to file
    account.save()

    logger.info(f"Account key reset done")


def doUpdateLicenseKey(license_key: str, logger=logging.Logger(__name__)):
    """
    Update license key, and reset account key
    :param license_key:
    :param logger:
    :return:
    """
    logger.info(f"Update license key: {license_key}")

    # Get current account
    account = getCurrentAccount(logger)

    if account.license_key == license_key:
        logger.warning(f"License key is the same, no need to update")
        return

    # Update license key
    updateLicenseKey(account, license_key)

    # Save changes to account
    account.license_key = license_key
    account.save()

    # Account needs to be reset after license key update
    resetAccountKey(logger)

    logger.info(f"License key updated")
