// We want to check that the input is in the form:
               // protectedData := IV || Enc(Kenc, IV, clearData) || Sign(Kval, IV || Enc(Kenc, IV, clearData))

               // Definitions used in this method:
               // encryptedPayload := Enc(Kenc, IV, clearData)
               // signature := Sign(Kval, IV || encryptedPayload)

               // These SymmetricAlgorithm instances are single-use; we wrap it in a 'using' block.
               using (SymmetricAlgorithm decryptionAlgorithm = _cryptoAlgorithmFactory.GetEncryptionAlgorithm()) {
                   decryptionAlgorithm.Key = _encryptionKey.GetKeyMaterial();

                   // These KeyedHashAlgorithm instances are single-use; we wrap it in a 'using' block.
                   using (KeyedHashAlgorithm validationAlgorithm = _cryptoAlgorithmFactory.GetValidationAlgorithm()) {
                       validationAlgorithm.Key = _validationKey.GetKeyMaterial();

                       // First, we need to verify that protectedData is even long enough to contain
                       // the required components (IV, encryptedPayload, signature).

                       int ivByteCount = decryptionAlgorithm.BlockSize / 8; // IV length is equal to the block size
                       int signatureByteCount = validationAlgorithm.HashSize / 8;
                       int encryptedPayloadByteCount = protectedData.Length - ivByteCount - signatureByteCount;
                       if (encryptedPayloadByteCount <= 0) {
                           // protectedData doesn't meet minimum length requirements
                           return null;
                       }

                       // If that check passes, we need to detect payload tampering.

                       // Compute the signature over the IV and encrypted payload
                       // computedSignature := Sign(Kval, IV || encryptedPayload)
                       byte[] computedSignature = validationAlgorithm.ComputeHash(protectedData, 0, ivByteCount + encryptedPayloadByteCount);

                       if (!CryptoUtil.BuffersAreEqual(
                           buffer1: protectedData, buffer1Offset: ivByteCount + encryptedPayloadByteCount, buffer1Count: signatureByteCount,
                           buffer2: computedSignature, buffer2Offset: 0, buffer2Count: computedSignature.Length)) {

                           // the computed signature didn't match the incoming signature, which is a sign of payload tampering
                           return null;
                       }
