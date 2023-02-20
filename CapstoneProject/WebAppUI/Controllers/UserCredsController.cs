using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using WebAppUI.Data;
using WebAppUI.Models;

namespace WebAppUI.Controllers
{
    public class UserCredsController : Controller
    {
        private readonly ApplicationDbContext _context;

        public UserCredsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // GET: UserCreds
        public async Task<IActionResult> Index()
        {
              return View(await _context.UserCreds.ToListAsync());
        }

        // GET: UserCreds/Details/5
        public async Task<IActionResult> Details(int? id)
        {
            if (id == null || _context.UserCreds == null)
            {
                return NotFound();
            }

            var userCreds = await _context.UserCreds
                .FirstOrDefaultAsync(m => m.ID == id);
            if (userCreds == null)
            {
                return NotFound();
            }

            return View(userCreds);
        }

        // GET: UserCreds/Create
        public IActionResult Create()
        {
            return View();
        }

        // POST: UserCreds/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("ID,FirstName,LastName,Password")] UserCreds userCreds)
        {
            if (ModelState.IsValid)
            {
                _context.Add(userCreds);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(userCreds);
        }

        // GET: UserCreds/Edit/5
        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null || _context.UserCreds == null)
            {
                return NotFound();
            }

            var userCreds = await _context.UserCreds.FindAsync(id);
            if (userCreds == null)
            {
                return NotFound();
            }
            return View(userCreds);
        }

        // POST: UserCreds/Edit/5
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("ID,FirstName,LastName,Password")] UserCreds userCreds)
        {
            if (id != userCreds.ID)
            {
                return NotFound();
            }

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(userCreds);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!UserCredsExists(userCreds.ID))
                    {
                        return NotFound();
                    }
                    else
                    {
                        throw;
                    }
                }
                return RedirectToAction(nameof(Index));
            }
            return View(userCreds);
        }

        // GET: UserCreds/Delete/5
        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null || _context.UserCreds == null)
            {
                return NotFound();
            }

            var userCreds = await _context.UserCreds
                .FirstOrDefaultAsync(m => m.ID == id);
            if (userCreds == null)
            {
                return NotFound();
            }

            return View(userCreds);
        }

        // POST: UserCreds/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            if (_context.UserCreds == null)
            {
                return Problem("Entity set 'ApplicationDbContext.UserCreds'  is null.");
            }
            var userCreds = await _context.UserCreds.FindAsync(id);
            if (userCreds != null)
            {
                _context.UserCreds.Remove(userCreds);
            }
            
            await _context.SaveChangesAsync();
            return RedirectToAction(nameof(Index));
        }

        private bool UserCredsExists(int id)
        {
          return _context.UserCreds.Any(e => e.ID == id);
        }
    }
}
