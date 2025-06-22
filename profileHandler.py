from flask import redirect, render_template, session, url_for, request, flash
from forms import DeleteUserForm, UpdateProfileForm, ChangePasswordForm
import databaseManagement as dbHandler
from werkzeug.security import generate_password_hash, check_password_hash


def handle_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    deleteUserForm = DeleteUserForm()
    user = dbHandler.retrieveUserByUsername(username)

    updateForm = UpdateProfileForm(
        data={
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    )
    passwordForm = ChangePasswordForm()

    if request.method == "POST":
        if "update_profile" in request.form:
            updateForm = UpdateProfileForm(request.form)
            if updateForm.validate():
                dbHandler.update_user_profile(
                    username,
                    updateForm.email.data,
                    updateForm.full_name.data,
                    updateForm.role.data,
                    user['password']
                )
                session['role'] = updateForm.role.data
                flash("Profile updated successfully.", "success")
                # Refresh user info
                user = dbHandler.retrieveUserByUsername(username)
                updateForm = UpdateProfileForm(
                    data={
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "role": user["role"]
                    }
                )
            else:
                flash("Please correct the errors in the profile form.", "danger")
        elif "change_password" in request.form:
            passwordForm = ChangePasswordForm(request.form)
            if passwordForm.validate():
                if not check_password_hash(user['password'], passwordForm.current_password.data):
                    flash("Current password is incorrect.", "danger")
                else:
                    hashed_password = generate_password_hash(passwordForm.new_password.data)
                    dbHandler.update_user_profile(
                        username,
                        user["email"],
                        user["full_name"],
                        user["role"],
                        hashed_password
                    )
                    flash("Password changed successfully.", "success")
                    passwordForm = ChangePasswordForm()  # Clear form
            else:
                flash("Please correct the errors in the password form.", "danger")

    return render_template(
        "/profile.html",
        username=username,
        form=deleteUserForm,
        updateForm=updateForm,
        passwordForm=passwordForm
    )

def deleteData(app):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if request.method == "POST":
        dbHandler.delete_user_by_username(username)
        session.pop('username', None)
        flash("Your account and data have been deleted.", "success")
        return redirect(url_for('login'))
    return redirect(url_for('profile'))