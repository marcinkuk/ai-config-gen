import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  console.log('ai-config-gen extension is now active!');

  const disposable = vscode.commands.registerCommand(
    'aiConfigGen.generate',
    async () => {
      const workspaceFolders = vscode.workspace.workspaceFolders;
      if (!workspaceFolders || workspaceFolders.length === 0) {
        vscode.window.showErrorMessage('No workspace folder open. Open a project first.');
        return;
      }

      const targetDir = workspaceFolders[0].uri.fsPath;
      const outputFormats = vscode.workspace.getConfiguration('aiConfigGen').get<string[]>('outputFormats', ['.claude.md', '.cursorrules', '.windsurfrules']);

      vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Generating AI config files...',
      }, async () => {
        try {
          const result = await spawnConfigGen(targetDir, outputFormats);
          if (result.success) {
            vscode.window.showInformationMessage(`Generated ${result.files.length} config file(s). Open them to review.`);
            // Open generated files
            for (const file of result.files) {
              const doc = await vscode.workspace.openTextDocument(file);
              await vscode.window.showTextDocument(doc, { preview: false });
            }
          } else {
            vscode.window.showErrorMessage(`ai-config-gen failed: ${result.error}`);
          }
        } catch (e) {
          vscode.window.showErrorMessage(`Error: ${e instanceof Error ? e.message : 'Unknown error'}`);
        }
      });
    }
  );

  context.subscriptions.push(disposable);
}

async function spawnConfigGen(targetDir: string, formats: string[]): Promise<{ success: boolean; files?: string[]; error?: string }> {
  const { spawn } = await import('child_process');
  const path = await import('path');

  return new Promise((resolve) => {
    // Try to run the installed CLI
    const child = spawn('ai-config-gen', [targetDir], { shell: true });

    const stdoutParts: string[] = [];
    const stderrParts: string[] = [];

    child.stdout.on('data', (d: Buffer) => stdoutParts.push(d.toString()));
    child.stderr.on('data', (d: Buffer) => stderrParts.push(d.toString()));

    child.on('close', (code) => {
      if (code === 0) {
        const generated = formats.map((f) => path.join(targetDir, f));
        resolve({ success: true, files: generated });
      } else {
        resolve({
          success: false,
          error: `Exit code ${code}. ${stderrParts.join('').slice(0, 200)}\nMake sure ai-config-gen is installed (pip install ai-config-gen).`,
        });
      }
    });
  });
}

export function deactivate() {}