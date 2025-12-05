# iCloud-test
Icloud Test
You are tasked with systematically reading EVERY SINGLE FILE in the iCloud-test folder

# CRITICAL REQUIREMENTS - NO EXCEPTIONS:

1. **Find ALL files** - Use bash to list every file in the directory (excluding .zip files)

2. **Read EVERY file COMPLETELY** - For each file:
   - First, count total lines using `wc -l`
   - If file is small (under 2000 lines), read it completely in one Read call
   - If file is large (2000+ lines), you MUST read it in chunks:
     * Calculate how many chunks needed (file has a ~25,000 token limit per read, approximately 1200-1500 lines safely)
     * Read chunk 1: lines 1-1200
     * Read chunk 2: lines 1201-2400
     * Read chunk 3: lines 2401-3600
     * Continue until you reach the LAST line of the file
     * DO NOT SKIP ANY CHUNKS
     * DO NOT STOP if you get a token error - reduce chunk size to 800 lines and retry

3. **Track your progress** - Maintain a detailed log showing:
   - Each file name
   - Total lines in that file
   - How many chunks you read
   - Line ranges for each chunk (e.g., "Read lines 1-1200, 1201-2400, 2401-3600...")
   - Confirmation that you reached the end of each file

4. **After reading everything** - Analyze ALL content together and identify:
   [YOUR SPECIFIC ANALYSIS TASK - e.g., "the most likely essay topics for a final exam"]

# VERIFICATION REQUIREMENT:

At the end of your response, include a table:

| File Name | Total Lines | Chunks Read | Line Ranges | Status |
|-----------|-------------|-------------|-------------|--------|
| file1.md  | 500         | 1           | 1-500       | ✅ Complete |
| file2.md  | 10954       | 9           | 1-1200, 1201-2400... | ✅ Complete |

Every file MUST show "✅ Complete" - NO EXCEPTIONS.

# WHAT TO RETURN TO ME:

1. Your verification table proving you read everything
2. A confirmation that you are ready to speak to the specific contents of the folder.

DO NOT STOP until you have read every single line of every single file. If you encounter any errors, adjust your approach and continue. COMPLETE THIS TASK FULLY.
